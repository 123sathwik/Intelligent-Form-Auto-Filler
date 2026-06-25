import React, { useState, useCallback, useRef } from 'react'
import { useLocation, Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  ArrowLeft, FileJson, Copy, Check, CheckCircle, AlertCircle, XCircle,
  RotateCcw, Undo, Download, Send, ChevronDown, ChevronRight,
  Sparkles, FileText, Table, Loader2, History, BarChart3,
  Info, Eye, EyeOff, FileDown
} from 'lucide-react'
import { toast } from 'react-toastify'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import apiClient from '@/services/api'

// ─── Types ────────────────────────────────────────────────────────────────────
interface FieldDef {
  id: string
  label: string
  type: string
  required?: boolean
  placeholder?: string
  options?: string[]
  entity_keys?: string[]
}

interface SectionDef {
  id: string
  title: string
  icon?: string
  fields: FieldDef[]
}

interface Schema {
  form_type: string
  sections: SectionDef[]
}

interface AutofillEntry {
  value: string
  source: 'auto' | 'empty'
}

type FieldStatus = 'auto' | 'edited' | 'empty'

// ─── Validation ───────────────────────────────────────────────────────────────
function validateFieldValue(field: FieldDef, value: string): string | null {
  if (field.required && !value.trim()) {
    return `${field.label} is required.`
  }
  if (!value.trim()) return null

  switch (field.type) {
    case 'email': {
      const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRe.test(value)) return 'Enter a valid email address.'
      break
    }
    case 'phone': {
      const phoneRe = /^[\d\s\+\-\(\)]{7,15}$/
      if (!phoneRe.test(value)) return 'Enter a valid phone number.'
      break
    }
    case 'date': {
      if (isNaN(Date.parse(value))) return 'Enter a valid date.'
      break
    }
    case 'number': {
      if (isNaN(Number(value))) return 'Enter a valid number.'
      break
    }
  }
  return null
}

// ─── Field Status Badge ───────────────────────────────────────────────────────
function StatusBadge({ status }: { status: FieldStatus }) {
  if (status === 'auto') return (
    <span className="flex items-center gap-1 text-[10px] font-bold text-emerald-400 bg-emerald-950/40 border border-emerald-800/50 px-2 py-0.5 rounded-full">
      <Sparkles size={9} /> AI Filled
    </span>
  )
  if (status === 'edited') return (
    <span className="flex items-center gap-1 text-[10px] font-bold text-yellow-400 bg-yellow-950/40 border border-yellow-700/40 px-2 py-0.5 rounded-full">
      <CheckCircle size={9} /> Edited
    </span>
  )
  return (
    <span className="flex items-center gap-1 text-[10px] font-bold text-red-400 bg-red-950/30 border border-red-800/30 px-2 py-0.5 rounded-full">
      <XCircle size={9} /> Empty
    </span>
  )
}

// ─── Single Field Row ─────────────────────────────────────────────────────────
interface FieldRowProps {
  field: FieldDef
  sectionId: string
  value: string
  originalValue: string
  error: string | null
  showHistory: boolean
  onChange: (sectionId: string, fieldId: string, val: string) => void
  onUndo: (sectionId: string, fieldId: string) => void
}

function FieldRow({ field, sectionId, value, originalValue, error, showHistory, onChange, onUndo }: FieldRowProps) {
  const isModified = value !== originalValue
  const isEmpty = !value.trim()
  const status: FieldStatus = isModified ? 'edited' : !isEmpty ? 'auto' : 'empty'

  const borderColor = error
    ? 'border-red-600/70 focus-within:border-red-500'
    : status === 'edited'
    ? 'border-yellow-500/60 focus-within:border-yellow-400'
    : status === 'auto'
    ? 'border-emerald-700/50 focus-within:border-emerald-500'
    : 'border-red-900/40 focus-within:border-red-600'

  const bgTint = error
    ? 'bg-red-950/10'
    : status === 'edited'
    ? 'bg-yellow-950/10'
    : status === 'auto'
    ? 'bg-emerald-950/10'
    : 'bg-red-950/5'

  const inputClass = `w-full ${bgTint} text-slate-100 text-sm font-medium placeholder-slate-600 outline-none px-3 py-2.5 rounded-xl border transition-all duration-200 ${borderColor}`

  return (
    <div className="space-y-1.5">
      {/* Label Row */}
      <div className="flex items-center justify-between gap-2 min-h-[20px]">
        <label className="text-xs font-bold text-slate-400 flex items-center gap-1">
          {field.label}
          {field.required && <span className="text-red-400">*</span>}
        </label>
        <div className="flex items-center gap-1.5">
          <StatusBadge status={status} />
          {isModified && (
            <button
              type="button"
              title="Undo to AI value"
              onClick={() => onUndo(sectionId, field.id)}
              className="p-0.5 text-slate-600 hover:text-yellow-400 transition-colors"
            >
              <Undo size={12} />
            </button>
          )}
        </div>
      </div>

      {/* Input */}
      {field.type === 'textarea' ? (
        <textarea
          value={value}
          onChange={e => onChange(sectionId, field.id, e.target.value)}
          placeholder={field.placeholder || ''}
          rows={3}
          className={`${inputClass} resize-none`}
        />
      ) : field.type === 'dropdown' && field.options ? (
        <select
          value={value}
          onChange={e => onChange(sectionId, field.id, e.target.value)}
          className={`${inputClass} cursor-pointer`}
        >
          <option value="">— Select —</option>
          {field.options.map(opt => <option key={opt} value={opt}>{opt}</option>)}
        </select>
      ) : (
        <input
          type={field.type === 'email' ? 'email' : field.type === 'number' ? 'number' : field.type === 'date' ? 'date' : 'text'}
          value={value}
          onChange={e => onChange(sectionId, field.id, e.target.value)}
          placeholder={field.placeholder || ''}
          className={inputClass}
        />
      )}

      {/* Error */}
      {error && (
        <motion.p
          initial={{ opacity: 0, y: -4 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-[11px] text-red-400 flex items-center gap-1"
        >
          <AlertCircle size={11} /> {error}
        </motion.p>
      )}

      {/* Edit History */}
      {showHistory && isModified && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="bg-slate-900/60 border border-slate-800 rounded-lg px-3 py-2 text-[10px] space-y-1"
        >
          <div className="flex items-center gap-1.5 text-slate-500">
            <History size={10} /> <span className="font-bold">Edit History</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-emerald-500 font-semibold">Original AI:</span>
            <span className="text-slate-400 font-mono">{originalValue || '(empty)'}</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-yellow-400 font-semibold">Your Edit:</span>
            <span className="text-slate-200 font-mono">{value || '(empty)'}</span>
          </div>
        </motion.div>
      )}
    </div>
  )
}

// ─── Summary Panel ────────────────────────────────────────────────────────────
interface SummaryPanelProps {
  totalFields: number
  autoFilled: number
  userEdited: number
  emptyFields: number
}

function SummaryPanel({ totalFields, autoFilled, userEdited, emptyFields }: SummaryPanelProps) {
  const filled = autoFilled + userEdited
  const completion = totalFields > 0 ? Math.round((filled / totalFields) * 100) : 0

  const stats = [
    { label: 'Total Fields', value: totalFields, color: 'text-slate-300', bg: 'bg-slate-800/50' },
    { label: 'AI Filled', value: autoFilled, color: 'text-emerald-400', bg: 'bg-emerald-950/40' },
    { label: 'Edited', value: userEdited, color: 'text-yellow-400', bg: 'bg-yellow-950/40' },
    { label: 'Empty', value: emptyFields, color: 'text-red-400', bg: 'bg-red-950/30' },
  ]

  return (
    <div className="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-4 space-y-4">
      <div className="flex items-center gap-2">
        <BarChart3 size={14} className="text-violet-400" />
        <span className="text-sm font-bold text-slate-200">Form Summary</span>
      </div>

      <div className="grid grid-cols-2 gap-2">
        {stats.map(s => (
          <div key={s.label} className={`${s.bg} rounded-xl p-3 border border-white/5`}>
            <p className={`text-xl font-black ${s.color}`}>{s.value}</p>
            <p className="text-[10px] text-slate-500 font-semibold mt-0.5">{s.label}</p>
          </div>
        ))}
      </div>

      {/* Completion bar */}
      <div className="space-y-1.5">
        <div className="flex justify-between items-center">
          <span className="text-[11px] font-bold text-slate-400">Completion</span>
          <span className={`text-sm font-black ${completion >= 80 ? 'text-emerald-400' : completion >= 50 ? 'text-yellow-400' : 'text-red-400'}`}>
            {completion}%
          </span>
        </div>
        <div className="h-2.5 bg-slate-800 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${completion}%` }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
            className={`h-full rounded-full ${
              completion >= 80 ? 'bg-gradient-to-r from-emerald-500 to-teal-500'
              : completion >= 50 ? 'bg-gradient-to-r from-yellow-500 to-amber-500'
              : 'bg-gradient-to-r from-red-500 to-rose-500'
            }`}
          />
        </div>
        {completion < 100 && (
          <p className="text-[10px] text-slate-500">
            {emptyFields} field{emptyFields !== 1 ? 's' : ''} remaining to complete
          </p>
        )}
        {completion === 100 && (
          <p className="text-[10px] text-emerald-400 font-semibold flex items-center gap-1">
            <CheckCircle size={11} /> All fields completed!
          </p>
        )}
      </div>
    </div>
  )
}

// ─── Export Dropdown ──────────────────────────────────────────────────────────
interface ExportMenuProps {
  onExportJSON: () => void
  onExportCSV: () => void
  onExportPDF: () => void
  disabled?: boolean
}

function ExportMenu({ onExportJSON, onExportCSV, onExportPDF, disabled }: ExportMenuProps) {
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  return (
    <div className="relative" ref={ref}>
      <button
        type="button"
        disabled={disabled}
        onClick={() => setOpen(p => !p)}
        className="flex items-center gap-2 px-5 py-3 bg-slate-900 border border-slate-700 text-slate-300 hover:text-white hover:border-slate-600 font-bold text-sm rounded-2xl transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
      >
        <FileDown size={15} /> Export
        <ChevronDown size={13} className={`transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: -8, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -8, scale: 0.96 }}
            className="absolute bottom-full mb-2 left-0 w-44 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl overflow-hidden z-50"
          >
            {[
              { label: 'Export JSON', icon: FileJson, action: () => { onExportJSON(); setOpen(false) } },
              { label: 'Export CSV', icon: Table, action: () => { onExportCSV(); setOpen(false) } },
              { label: 'Export PDF', icon: FileText, action: () => { onExportPDF(); setOpen(false) } },
            ].map(item => (
              <button
                key={item.label}
                type="button"
                onClick={item.action}
                className="w-full flex items-center gap-2.5 px-4 py-3 text-sm font-semibold text-slate-300 hover:bg-slate-800 hover:text-white transition-colors"
              >
                <item.icon size={14} className="text-violet-400" />
                {item.label}
              </button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

// ─── Main Review Page ─────────────────────────────────────────────────────────
export default function FormReview() {
  const location = useLocation()

  const schema: Schema = location.state?.schema || null
  const initialFormData: Record<string, Record<string, string>> = location.state?.formData || {}
  const autofillMap: Record<string, AutofillEntry> = location.state?.autofillMap || {}
  const serverStats = location.state?.stats || null
  const formType = location.state?.formType || 'Document'
  const filename = location.state?.filename || 'Unknown File'

  const buildInitialState = useCallback(() => {
    if (!schema?.sections?.length) return initialFormData
    const state: Record<string, Record<string, string>> = {}
    for (const section of schema.sections) {
      state[section.id] = {}
      for (const field of section.fields) {
        const key = `${section.id}.${field.id}`
        state[section.id][field.id] = autofillMap[key]?.value ?? initialFormData?.[section.id]?.[field.id] ?? ''
      }
    }
    return state
  }, [schema, initialFormData, autofillMap])

  const [formData, setFormData] = useState<Record<string, Record<string, string>>>(buildInitialState)
  const [originalData] = useState<Record<string, Record<string, string>>>(buildInitialState)
  const [history, setHistory] = useState<any[]>([])
  const [errors, setErrors] = useState<Record<string, string | null>>({})
  const [collapsedSections, setCollapsedSections] = useState<Set<string>>(new Set())
  const [showHistory, setShowHistory] = useState(false)
  const [copied, setCopied] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  const [submittedAt, setSubmittedAt] = useState('')

  const deepClone = (obj: any) => JSON.parse(JSON.stringify(obj))

  // ─── Derived Stats ──────────────────────────────────────────────────────
  const computeStats = () => {
    let totalFields = 0, autoFilled = 0, userEdited = 0, emptyFields = 0
    if (!schema?.sections) return { totalFields, autoFilled, userEdited, emptyFields }
    for (const section of schema.sections) {
      for (const field of section.fields) {
        totalFields++
        const key = `${section.id}.${field.id}`
        const curVal = formData[section.id]?.[field.id] ?? ''
        const origVal = originalData[section.id]?.[field.id] ?? ''
        const wasAuto = autofillMap[key]?.source === 'auto'
        const isModified = curVal !== origVal

        if (isModified) userEdited++
        else if (wasAuto && curVal) autoFilled++
        else if (!curVal.trim()) emptyFields++
        else autoFilled++
      }
    }
    return { totalFields, autoFilled, userEdited, emptyFields }
  }
  const stats = computeStats()

  // ─── Handlers ──────────────────────────────────────────────────────────
  const handleChange = useCallback((sectionId: string, fieldId: string, val: string) => {
    setHistory(prev => [...prev, deepClone(formData)])
    setFormData(prev => ({ ...prev, [sectionId]: { ...prev[sectionId], [fieldId]: val } }))
    // Clear error on change
    setErrors(prev => ({ ...prev, [`${sectionId}.${fieldId}`]: null }))
  }, [formData])

  const handleUndo = useCallback((sectionId: string, fieldId: string) => {
    setHistory(prev => [...prev, deepClone(formData)])
    setFormData(prev => ({
      ...prev,
      [sectionId]: { ...prev[sectionId], [fieldId]: originalData[sectionId]?.[fieldId] ?? '' }
    }))
    setErrors(prev => ({ ...prev, [`${sectionId}.${fieldId}`]: null }))
  }, [formData, originalData])

  const handleUndoLast = () => {
    if (!history.length) return
    const prev = history[history.length - 1]
    setHistory(h => h.slice(0, -1))
    setFormData(prev)
  }

  const handleReset = () => {
    setFormData(deepClone(originalData))
    setHistory([])
    setErrors({})
    toast.info('Form reset to original AI values.')
  }

  const toggleSection = (id: string) => {
    setCollapsedSections(prev => { const n = new Set(prev); n.has(id) ? n.delete(id) : n.add(id); return n })
  }

  // ─── Validation ──────────────────────────────────────────────────────────
  const validateAll = (): boolean => {
    if (!schema?.sections) return true
    const newErrors: Record<string, string | null> = {}
    let hasError = false
    for (const section of schema.sections) {
      for (const field of section.fields) {
        const val = formData[section.id]?.[field.id] ?? ''
        const err = validateFieldValue(field, val)
        const key = `${section.id}.${field.id}`
        newErrors[key] = err
        if (err) hasError = true
      }
    }
    setErrors(newErrors)
    if (hasError) {
      // Expand sections with errors
      const sectionsWithErrors = new Set<string>()
      for (const key of Object.keys(newErrors)) {
        if (newErrors[key]) {
          const sectionId = key.split('.')[0]
          sectionsWithErrors.add(sectionId)
        }
      }
      setCollapsedSections(prev => {
        const n = new Set(prev)
        sectionsWithErrors.forEach(id => n.delete(id))
        return n
      })
    }
    return !hasError
  }

  // ─── Submit ──────────────────────────────────────────────────────────────
  const handleSubmit = async () => {
    const valid = validateAll()
    if (!valid) {
      toast.error('Please fix validation errors before submitting.')
      return
    }

    setIsSubmitting(true)
    try {
      const res: any = await apiClient.post('/submit', {
        form_type: formType,
        filename,
        form_data: formData,
        autofill_map: autofillMap,
        stats: { ...stats, completion: stats.totalFields > 0 ? Math.round(((stats.autoFilled + stats.userEdited) / stats.totalFields) * 100) : 0 }
      })

      setSubmitted(true)
      setSubmittedAt(res.submitted_at || new Date().toISOString())
      toast.success(`Form submitted! Saved as: ${res.filename}`)
    } catch (err: any) {
      toast.error(err.message || 'Submission failed. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  // ─── Export JSON ─────────────────────────────────────────────────────────
  const handleExportJSON = () => {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    const payload = {
      form_type: formType,
      source_file: filename,
      exported_at: new Date().toISOString(),
      form_data: formData,
      stats
    }
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${timestamp}_${formType.replace(/\s+/g, '_').toLowerCase()}.json`
    a.click()
    URL.revokeObjectURL(url)
    toast.success('JSON exported!')
  }

  // ─── Export CSV ──────────────────────────────────────────────────────────
  const handleExportCSV = () => {
    if (!schema?.sections) return
    const rows: string[][] = [['Section', 'Field', 'Value', 'Status']]
    for (const section of schema.sections) {
      for (const field of section.fields) {
        const key = `${section.id}.${field.id}`
        const val = formData[section.id]?.[field.id] ?? ''
        const origVal = originalData[section.id]?.[field.id] ?? ''
        const isModified = val !== origVal
        const wasAuto = autofillMap[key]?.source === 'auto'
        const status = isModified ? 'Edited' : wasAuto ? 'AI Filled' : val ? 'Filled' : 'Empty'
        rows.push([section.title, field.label, val, status])
      }
    }
    const csv = rows.map(r => r.map(c => `"${String(c).replace(/"/g, '""')}"`).join(',')).join('\n')
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${timestamp}_${formType.replace(/\s+/g, '_').toLowerCase()}.csv`
    a.click()
    URL.revokeObjectURL(url)
    toast.success('CSV exported!')
  }

  // ─── Export PDF ──────────────────────────────────────────────────────────
  const handleExportPDF = () => {
    if (!schema?.sections) return
    const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' })
    const pageW = doc.internal.pageSize.getWidth()
    const margin = 18

    // Header background
    doc.setFillColor(30, 20, 60)
    doc.rect(0, 0, pageW, 40, 'F')

    // Title
    doc.setFontSize(20)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(220, 200, 255)
    doc.text(formType, margin, 18)

    // Subtitle
    doc.setFontSize(9)
    doc.setFont('helvetica', 'normal')
    doc.setTextColor(150, 130, 200)
    doc.text(`Source: ${filename}`, margin, 25)
    doc.text(`Submitted: ${new Date().toLocaleString()}`, margin, 30)

    // Stats bar
    const completion = stats.totalFields > 0 ? Math.round(((stats.autoFilled + stats.userEdited) / stats.totalFields) * 100) : 0
    doc.setFontSize(8)
    doc.setTextColor(180, 180, 180)
    doc.text(
      `Fields: ${stats.totalFields}  |  AI Filled: ${stats.autoFilled}  |  Edited: ${stats.userEdited}  |  Empty: ${stats.emptyFields}  |  Completion: ${completion}%`,
      margin,
      36
    )

    let y = 50

    // Sections
    for (const section of schema.sections) {
      const fields = section.fields.filter(f => formData[section.id]?.[f.id] !== undefined)
      if (!fields.length) continue

      // Section title
      if (y > 250) { doc.addPage(); y = 20 }
      doc.setFillColor(45, 30, 80)
      doc.roundedRect(margin - 2, y - 5, pageW - margin * 2 + 4, 10, 2, 2, 'F')
      doc.setFontSize(10)
      doc.setFont('helvetica', 'bold')
      doc.setTextColor(210, 190, 255)
      doc.text(section.title, margin + 2, y + 1.5)
      y += 10

      // Table rows
      const tableRows = fields.map(field => {
        const key = `${section.id}.${field.id}`
        const val = formData[section.id]?.[field.id] ?? ''
        const origVal = originalData[section.id]?.[field.id] ?? ''
        const isModified = val !== origVal
        const wasAuto = autofillMap[key]?.source === 'auto'
        const status = isModified ? 'Edited' : wasAuto ? 'AI' : val ? 'Filled' : '—'
        return [field.label, val || '—', status]
      })

      ;(doc as any).autoTable({
        startY: y,
        head: [['Field', 'Value', 'Source']],
        body: tableRows,
        margin: { left: margin, right: margin },
        styles: { fontSize: 9, cellPadding: 3, textColor: [200, 200, 200], fillColor: [15, 15, 30], lineColor: [50, 50, 80] },
        headStyles: { fillColor: [50, 30, 90], textColor: [200, 180, 255], fontStyle: 'bold', fontSize: 9 },
        alternateRowStyles: { fillColor: [20, 15, 40] },
        columnStyles: {
          0: { cellWidth: 55, fontStyle: 'bold', textColor: [170, 160, 220] },
          1: { cellWidth: 'auto' },
          2: { cellWidth: 22, halign: 'center' }
        },
        didDrawPage: (data: any) => { y = data.cursor.y + 6 }
      })

      y = (doc as any).lastAutoTable.finalY + 8
    }

    // Footer
    const pageCount = doc.internal.getNumberOfPages()
    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i)
      doc.setFontSize(7)
      doc.setTextColor(100, 100, 130)
      doc.text(`Intelligent Form Auto-Filler  |  Page ${i} of ${pageCount}`, margin, doc.internal.pageSize.getHeight() - 8)
    }

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
    doc.save(`${timestamp}_${formType.replace(/\s+/g, '_').toLowerCase()}.pdf`)
    toast.success('PDF exported!')
  }

  // ─── Copy JSON ───────────────────────────────────────────────────────────
  const handleCopyJSON = () => {
    navigator.clipboard.writeText(JSON.stringify(formData, null, 2))
      .then(() => { setCopied(true); toast.success('JSON copied!'); setTimeout(() => setCopied(false), 2000) })
      .catch(() => toast.error('Failed to copy'))
  }

  // ─── No schema fallback ──────────────────────────────────────────────────
  if (!schema || !schema.sections?.length) {
    return (
      <div className="space-y-6 py-4">
        <div className="flex items-center gap-3">
          <Link to="/upload" className="p-2 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-400 rounded-xl transition-colors">
            <ArrowLeft size={16} />
          </Link>
          <h1 className="text-2xl font-extrabold text-slate-100">Form Review</h1>
        </div>
        <div className="bg-slate-900/30 border border-slate-800 rounded-3xl p-6">
          <pre className="text-xs text-violet-200 font-mono overflow-auto">{JSON.stringify(initialFormData, null, 2)}</pre>
        </div>
      </div>
    )
  }

  const hasErrors = Object.values(errors).some(Boolean)

  // ─── Submission Success Screen ────────────────────────────────────────────
  if (submitted) {
    const completion = stats.totalFields > 0 ? Math.round(((stats.autoFilled + stats.userEdited) / stats.totalFields) * 100) : 0
    return (
      <div className="flex flex-col items-center justify-center min-h-[70vh] space-y-8 py-8">
        <motion.div
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ type: 'spring', stiffness: 260, damping: 20 }}
          className="w-24 h-24 rounded-full bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-2xl shadow-emerald-500/40"
        >
          <CheckCircle size={48} className="text-white" />
        </motion.div>
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="text-center space-y-3">
          <h1 className="text-4xl font-extrabold tracking-tight bg-gradient-to-r from-emerald-300 to-teal-200 bg-clip-text text-transparent">
            Form Submitted!
          </h1>
          <p className="text-slate-400 text-sm">Your completed form has been saved successfully.</p>
          <div className="flex flex-wrap items-center justify-center gap-4 mt-4 text-xs text-slate-400">
            <span>Form Type: <span className="text-violet-300 font-bold">{formType}</span></span>
            <span>Completion: <span className="text-emerald-400 font-bold">{completion}%</span></span>
            <span>Submitted: <span className="text-slate-300 font-mono">{new Date(submittedAt).toLocaleString()}</span></span>
          </div>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="flex gap-3 flex-wrap justify-center">
          <button
            onClick={handleExportJSON}
            className="flex items-center gap-2 px-5 py-3 bg-slate-900 border border-slate-700 text-slate-300 hover:text-white rounded-2xl font-bold text-sm transition-colors"
          >
            <FileJson size={15} /> Export JSON
          </button>
          <button
            onClick={handleExportCSV}
            className="flex items-center gap-2 px-5 py-3 bg-slate-900 border border-slate-700 text-slate-300 hover:text-white rounded-2xl font-bold text-sm transition-colors"
          >
            <Table size={15} /> Export CSV
          </button>
          <button
            onClick={handleExportPDF}
            className="flex items-center gap-2 px-5 py-3 bg-slate-900 border border-slate-700 text-slate-300 hover:text-white rounded-2xl font-bold text-sm transition-colors"
          >
            <FileText size={15} /> Export PDF
          </button>
          <Link
            to="/upload"
            className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 text-white rounded-2xl font-bold text-sm shadow-lg shadow-violet-500/25 transition-all"
          >
            <ArrowLeft size={15} /> Process Another Document
          </Link>
        </motion.div>
      </div>
    )
  }

  // ─── Main Review UI ───────────────────────────────────────────────────────
  return (
    <div className="space-y-5 py-4">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
        <div className="flex items-center gap-3.5">
          <Link to="/upload" className="p-2 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-400 rounded-xl transition-colors flex-shrink-0">
            <ArrowLeft size={16} />
          </Link>
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-violet-300 via-purple-200 to-white bg-clip-text text-transparent">
              Review & Submit
            </h1>
            <div className="flex flex-wrap items-center gap-3 mt-1.5 text-xs text-slate-400">
              <span>File: <span className="text-indigo-400 font-medium font-mono">{filename}</span></span>
              <span className="w-1.5 h-1.5 rounded-full bg-slate-700" />
              <span className="flex items-center gap-1.5 px-2.5 py-0.5 bg-violet-950/30 border border-violet-800/50 text-violet-300 rounded-full font-bold">
                {formType}
              </span>
            </div>
          </div>
        </div>

        {/* History toggle */}
        <button
          type="button"
          onClick={() => setShowHistory(p => !p)}
          className={`flex items-center gap-2 px-4 py-2 text-xs font-bold rounded-xl border transition-colors flex-shrink-0 ${
            showHistory
              ? 'bg-violet-950/40 border-violet-700/50 text-violet-300'
              : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700'
          }`}
        >
          <History size={13} />
          {showHistory ? 'Hide Edit History' : 'Show Edit History'}
        </button>
      </div>

      {/* Legend */}
      <div className="flex flex-wrap items-center gap-x-5 gap-y-2 px-1 text-[11px]">
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-emerald-500/70 border border-emerald-500 flex-shrink-0" />
          <span className="text-emerald-400 font-semibold">AI Auto-filled</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-yellow-500/60 border border-yellow-500 flex-shrink-0" />
          <span className="text-yellow-400 font-semibold">User Edited</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-3 h-3 rounded-full bg-red-600/50 border border-red-600 flex-shrink-0" />
          <span className="text-red-400 font-semibold">Empty</span>
        </div>
        <div className="flex items-center gap-1.5 text-slate-500">
          <Info size={11} />
          <span>Red <span className="text-red-400">*</span> = required field</span>
        </div>
      </div>

      {/* Validation error banner */}
      <AnimatePresence>
        {hasErrors && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="flex items-center gap-3 p-4 bg-red-950/30 border border-red-800/50 rounded-2xl"
          >
            <AlertCircle size={16} className="text-red-400 flex-shrink-0" />
            <p className="text-sm text-red-300 font-semibold">
              Please fix the validation errors below before submitting.
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">

        {/* Left — Form */}
        <div className="lg:col-span-7 space-y-4">

          {/* Action bar */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between p-4 bg-slate-900/40 border border-slate-800 rounded-2xl gap-3 backdrop-blur-md">
            <div className="flex items-center gap-2 flex-wrap">
              {stats.userEdited > 0 && (
                <span className="flex items-center text-xs font-bold text-yellow-400 bg-yellow-950/30 border border-yellow-800/40 px-3 py-1.5 rounded-xl">
                  <AlertCircle size={12} className="mr-1.5" />
                  {stats.userEdited} field{stats.userEdited > 1 ? 's' : ''} edited
                </span>
              )}
              {stats.emptyFields > 0 && (
                <span className="flex items-center text-xs font-bold text-red-400 bg-red-950/20 border border-red-800/30 px-3 py-1.5 rounded-xl">
                  <XCircle size={12} className="mr-1.5" />
                  {stats.emptyFields} empty
                </span>
              )}
              {stats.emptyFields === 0 && stats.userEdited === 0 && (
                <span className="flex items-center text-xs font-bold text-emerald-400 bg-emerald-950/20 border border-emerald-900/40 px-3 py-1.5 rounded-xl">
                  <CheckCircle size={12} className="mr-1.5" /> All fields filled
                </span>
              )}
            </div>
            <div className="flex items-center gap-2">
              <button
                type="button"
                disabled={!history.length}
                onClick={handleUndoLast}
                className="flex items-center px-4 py-2 text-xs font-semibold rounded-xl border border-slate-800 text-slate-300 bg-slate-900 hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
              >
                <Undo size={12} className="mr-1.5" /> Undo
              </button>
              <button
                type="button"
                disabled={stats.userEdited === 0}
                onClick={handleReset}
                className="flex items-center px-4 py-2 text-xs font-semibold rounded-xl border border-slate-800 text-slate-300 bg-slate-900 hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
              >
                <RotateCcw size={12} className="mr-1.5" /> Reset
              </button>
            </div>
          </div>

          {/* Form Sections */}
          {schema.sections.map(section => {
            const isCollapsed = collapsedSections.has(section.id)
            const sectionErrors = section.fields.filter(f => errors[`${section.id}.${f.id}`]).length
            const sectionAutoFilled = section.fields.filter(f => {
              const val = formData[section.id]?.[f.id] ?? ''
              const orig = originalData[section.id]?.[f.id] ?? ''
              return val && val === orig && autofillMap[`${section.id}.${f.id}`]?.source === 'auto'
            }).length

            return (
              <motion.div
                key={section.id}
                layout
                className="bg-slate-900/30 border border-slate-800/80 rounded-2xl overflow-hidden backdrop-blur-sm"
              >
                <button
                  type="button"
                  onClick={() => toggleSection(section.id)}
                  className="w-full flex items-center justify-between px-5 py-4 hover:bg-slate-800/30 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-violet-950/50 border border-violet-800/40 flex items-center justify-center flex-shrink-0">
                      <ChevronRight size={14} className="text-violet-400" />
                    </div>
                    <div className="text-left">
                      <p className="text-sm font-bold text-slate-200">{section.title}</p>
                      <div className="flex items-center gap-2 text-[10px] text-slate-500 mt-0.5">
                        <span>{section.fields.length} field{section.fields.length !== 1 ? 's' : ''}</span>
                        {sectionAutoFilled > 0 && <span className="text-emerald-500">· {sectionAutoFilled} AI filled</span>}
                        {sectionErrors > 0 && <span className="text-red-400 font-bold">· {sectionErrors} error{sectionErrors > 1 ? 's' : ''}</span>}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {sectionErrors > 0 && <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />}
                    <ChevronDown size={14} className={`text-slate-500 transition-transform ${isCollapsed ? '' : 'rotate-180'}`} />
                  </div>
                </button>

                <AnimatePresence>
                  {!isCollapsed && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="overflow-hidden"
                    >
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-5 pt-3 border-t border-slate-800/50">
                        {section.fields.map(field => {
                          const key = `${section.id}.${field.id}`
                          const curVal = formData[section.id]?.[field.id] ?? ''
                          const origVal = originalData[section.id]?.[field.id] ?? ''
                          const isLong = field.type === 'textarea'

                          return (
                            <div key={field.id} className={isLong ? 'sm:col-span-2' : ''}>
                              <FieldRow
                                field={field}
                                sectionId={section.id}
                                value={curVal}
                                originalValue={origVal}
                                error={errors[key] ?? null}
                                showHistory={showHistory}
                                onChange={handleChange}
                                onUndo={handleUndo}
                              />
                            </div>
                          )
                        })}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            )
          })}

          {/* Submit / Export Row */}
          <div className="flex items-center gap-3 pt-2">
            <ExportMenu
              onExportJSON={handleExportJSON}
              onExportCSV={handleExportCSV}
              onExportPDF={handleExportPDF}
            />
            <motion.button
              type="button"
              disabled={isSubmitting}
              onClick={handleSubmit}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex-1 flex items-center justify-center gap-2.5 px-7 py-3 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 text-white font-bold text-sm rounded-2xl shadow-lg shadow-violet-500/25 disabled:opacity-60 disabled:cursor-not-allowed transition-all"
            >
              {isSubmitting
                ? <><Loader2 size={15} className="animate-spin" /> Submitting...</>
                : <><Send size={15} /> Submit Form</>
              }
            </motion.button>
          </div>
        </div>

        {/* Right Panel — Summary + JSON */}
        <div className="lg:col-span-5 lg:sticky lg:top-6 space-y-4">

          {/* Summary Panel */}
          <SummaryPanel
            totalFields={stats.totalFields}
            autoFilled={stats.autoFilled}
            userEdited={stats.userEdited}
            emptyFields={stats.emptyFields}
          />

          {/* Live JSON preview */}
          <div className="bg-slate-900/30 border border-slate-800/80 rounded-3xl p-5 backdrop-blur-md flex flex-col" style={{ height: '50vh', minHeight: '350px' }}>
            <div className="flex justify-between items-center border-b border-slate-800/60 pb-3 mb-4 flex-shrink-0">
              <div className="flex items-center gap-2 text-slate-200 font-bold text-sm">
                <FileJson size={16} className="text-violet-400" />
                <span>Live JSON</span>
              </div>
              <button
                type="button"
                onClick={handleCopyJSON}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-950 border border-slate-800 text-slate-400 hover:text-slate-200 rounded-xl text-xs font-semibold hover:border-slate-700 transition-colors"
              >
                {copied
                  ? <><Check size={11} className="text-emerald-400" /><span className="text-emerald-400">Copied</span></>
                  : <><Copy size={11} /><span>Copy</span></>
                }
              </button>
            </div>
            <div className="flex-1 overflow-auto bg-slate-950/60 border border-slate-900 rounded-2xl p-4 font-mono text-[10.5px] leading-relaxed text-violet-200 select-all">
              <pre>{JSON.stringify(formData, null, 2)}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
