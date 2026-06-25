import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Plus, Trash2, GripVertical, ChevronDown, ChevronUp, FolderOpen } from 'lucide-react'

interface FieldDef {
  id: string
  label: string
  type: string
  required: boolean
  entity_keys: string[]
}

interface SectionDef {
  id: string
  title: string
  icon: string
  fields: FieldDef[]
}

interface Props {
  onChange: (schema: { sections: SectionDef[] } | null) => void
}

const FIELD_TYPES = [
  { value: 'text', label: 'Text' },
  { value: 'email', label: 'Email' },
  { value: 'phone', label: 'Phone' },
  { value: 'number', label: 'Number' },
  { value: 'date', label: 'Date' },
  { value: 'textarea', label: 'Long Text' },
  { value: 'dropdown', label: 'Dropdown' },
]

// Common entity keys the user can pick from
const ENTITY_KEY_OPTIONS = [
  'name', 'email', 'phone', 'dob', 'gender', 'nationality',
  'father_name', 'mother_name', 'address', 'city', 'state', 'pincode',
  'degree', 'branch', 'cgpa', 'percentage', 'college', 'university',
  'company', 'experience', 'skills', 'projects', 'certificates',
  'aadhaar_number', 'pan_number', 'passport_number', 'driving_license_number',
  'invoice_number', 'employee_id', 'roll_number', 'registration_number'
]

let sectionCounter = 1
let fieldCounter = 1

function makeSection(): SectionDef {
  return {
    id: `section_${sectionCounter++}`,
    title: '',
    icon: 'FolderOpen',
    fields: []
  }
}

function makeField(): FieldDef {
  return {
    id: `field_${fieldCounter++}`,
    label: '',
    type: 'text',
    required: false,
    entity_keys: []
  }
}

export default function CustomFormBuilder({ onChange }: Props) {
  const [sections, setSections] = useState<SectionDef[]>([makeSection()])
  const [collapsedSections, setCollapsedSections] = useState<Set<string>>(new Set())

  useEffect(() => {
    const hasContent = sections.some(s => s.title.trim() && s.fields.some(f => f.label.trim()))
    onChange(hasContent ? { sections } : null)
  }, [sections])

  const addSection = () => {
    setSections(prev => [...prev, makeSection()])
  }

  const updateSection = (id: string, key: keyof SectionDef, val: any) => {
    setSections(prev => prev.map(s => s.id === id ? { ...s, [key]: val } : s))
  }

  const removeSection = (id: string) => {
    setSections(prev => prev.filter(s => s.id !== id))
  }

  const addField = (sectionId: string) => {
    setSections(prev => prev.map(s =>
      s.id === sectionId ? { ...s, fields: [...s.fields, makeField()] } : s
    ))
  }

  const updateField = (sectionId: string, fieldId: string, key: keyof FieldDef, val: any) => {
    setSections(prev => prev.map(s =>
      s.id === sectionId
        ? { ...s, fields: s.fields.map(f => f.id === fieldId ? { ...f, [key]: val } : f) }
        : s
    ))
  }

  const removeField = (sectionId: string, fieldId: string) => {
    setSections(prev => prev.map(s =>
      s.id === sectionId ? { ...s, fields: s.fields.filter(f => f.id !== fieldId) } : s
    ))
  }

  const toggleCollapse = (id: string) => {
    setCollapsedSections(prev => {
      const next = new Set(prev)
      next.has(id) ? next.delete(id) : next.add(id)
      return next
    })
  }

  return (
    <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-slate-200">Custom Form Builder</h3>
          <p className="text-xs text-slate-500 mt-0.5">Define sections and fields for your form</p>
        </div>
        <button
          type="button"
          onClick={addSection}
          className="flex items-center gap-1.5 text-xs font-bold text-violet-400 bg-violet-950/30 border border-violet-800/40 hover:bg-violet-950/60 px-3 py-1.5 rounded-xl transition-colors"
        >
          <Plus size={13} /> Add Section
        </button>
      </div>

      <AnimatePresence>
        {sections.map((section, si) => {
          const isCollapsed = collapsedSections.has(section.id)
          return (
            <motion.div
              key={section.id}
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="border border-slate-700/60 rounded-xl overflow-hidden"
            >
              {/* Section Header */}
              <div className="flex items-center gap-3 p-3 bg-slate-800/40">
                <GripVertical size={14} className="text-slate-600 flex-shrink-0" />
                <input
                  type="text"
                  value={section.title}
                  onChange={e => updateSection(section.id, 'title', e.target.value)}
                  placeholder={`Section ${si + 1} Name (e.g. Personal Information)`}
                  className="flex-1 bg-transparent text-sm font-semibold text-slate-200 placeholder-slate-600 outline-none"
                />
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => toggleCollapse(section.id)}
                    className="p-1.5 text-slate-500 hover:text-slate-300 transition-colors"
                  >
                    {isCollapsed ? <ChevronDown size={14} /> : <ChevronUp size={14} />}
                  </button>
                  {sections.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeSection(section.id)}
                      className="p-1.5 text-slate-600 hover:text-rose-400 transition-colors"
                    >
                      <Trash2 size={14} />
                    </button>
                  )}
                </div>
              </div>

              {/* Section Fields */}
              <AnimatePresence>
                {!isCollapsed && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="p-3 space-y-2 bg-slate-900/20"
                  >
                    {section.fields.map((field) => (
                      <div key={field.id} className="flex items-center gap-2 p-2.5 bg-slate-800/30 border border-slate-700/40 rounded-xl">
                        <GripVertical size={12} className="text-slate-700 flex-shrink-0" />

                        {/* Field Label */}
                        <input
                          type="text"
                          value={field.label}
                          onChange={e => updateField(section.id, field.id, 'label', e.target.value)}
                          placeholder="Field label"
                          className="flex-1 min-w-0 bg-transparent text-xs font-semibold text-slate-300 placeholder-slate-600 outline-none"
                        />

                        {/* Field Type */}
                        <select
                          value={field.type}
                          onChange={e => updateField(section.id, field.id, 'type', e.target.value)}
                          className="text-[11px] bg-slate-800 border border-slate-700 text-slate-300 rounded-lg px-2 py-1 outline-none"
                        >
                          {FIELD_TYPES.map(t => (
                            <option key={t.value} value={t.value}>{t.label}</option>
                          ))}
                        </select>

                        {/* Entity Key */}
                        <select
                          value={field.entity_keys[0] || ''}
                          onChange={e => updateField(section.id, field.id, 'entity_keys', e.target.value ? [e.target.value] : [])}
                          className="text-[11px] bg-slate-800 border border-slate-700 text-slate-400 rounded-lg px-2 py-1 outline-none max-w-[130px]"
                        >
                          <option value="">— Auto-fill Key —</option>
                          {ENTITY_KEY_OPTIONS.map(k => (
                            <option key={k} value={k}>{k}</option>
                          ))}
                        </select>

                        {/* Required toggle */}
                        <label className="flex items-center gap-1 cursor-pointer flex-shrink-0">
                          <input
                            type="checkbox"
                            checked={field.required}
                            onChange={e => updateField(section.id, field.id, 'required', e.target.checked)}
                            className="w-3.5 h-3.5 accent-violet-500"
                          />
                          <span className="text-[10px] text-slate-500">Req</span>
                        </label>

                        <button
                          type="button"
                          onClick={() => removeField(section.id, field.id)}
                          className="p-1 text-slate-600 hover:text-rose-400 transition-colors flex-shrink-0"
                        >
                          <Trash2 size={13} />
                        </button>
                      </div>
                    ))}

                    <button
                      type="button"
                      onClick={() => addField(section.id)}
                      className="w-full flex items-center justify-center gap-1.5 text-[11px] font-semibold text-slate-500 hover:text-violet-400 border border-dashed border-slate-700 hover:border-violet-700/50 rounded-xl py-2 transition-colors"
                    >
                      <Plus size={12} /> Add Field
                    </button>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          )
        })}
      </AnimatePresence>
    </div>
  )
}
