import { useState, useRef, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  FileText, Globe, Fingerprint, CreditCard, Car, HeartPulse,
  Receipt, Landmark, School, Shield, Briefcase, Users, Puzzle,
  Upload as UploadIcon, File, X, CheckCircle, AlertTriangle,
  ChevronRight, ChevronLeft, Loader2, Cpu, Zap, Brain, Layers,
  ArrowRight, Plus, Trash2, GripVertical, Image as ImageIcon,
  CheckCheck, ClipboardList
} from 'lucide-react'
import { toast } from 'react-toastify'
import apiClient from '@/services/api'
import CustomFormBuilder from '@/components/CustomFormBuilder'

// ─── Constants ────────────────────────────────────────────────────────────────
const MAX_FILE_SIZE = 20 * 1024 * 1024
const ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.jpg', '.jpeg', '.png']
const ALLOWED_MIME_TYPES = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'image/jpeg',
  'image/png'
]

// ─── Form Type Definitions ────────────────────────────────────────────────────
const FORM_TYPES = [
  { id: 'Resume', label: 'Resume', icon: FileText, color: 'from-violet-500 to-purple-600', description: 'CV / job application' },
  { id: 'Passport', label: 'Passport', icon: Globe, color: 'from-blue-500 to-cyan-600', description: 'Travel document' },
  { id: 'Aadhaar', label: 'Aadhaar', icon: Fingerprint, color: 'from-orange-500 to-amber-600', description: 'Unique identity number' },
  { id: 'PAN Card', label: 'PAN Card', icon: CreditCard, color: 'from-emerald-500 to-teal-600', description: 'Income tax identity' },
  { id: 'Driving License', label: 'Driving License', icon: Car, color: 'from-sky-500 to-blue-600', description: 'Driving authorization' },
  { id: 'Medical Report', label: 'Medical Report', icon: HeartPulse, color: 'from-rose-500 to-red-600', description: 'Patient health record' },
  { id: 'Invoice', label: 'Invoice', icon: Receipt, color: 'from-yellow-500 to-amber-600', description: 'Business billing' },
  { id: 'Bank KYC', label: 'Bank KYC', icon: Landmark, color: 'from-indigo-500 to-violet-600', description: 'Account verification' },
  { id: 'Admission Form', label: 'Admission Form', icon: School, color: 'from-teal-500 to-cyan-600', description: 'College / university' },
  { id: 'Insurance Claim', label: 'Insurance Claim', icon: Shield, color: 'from-pink-500 to-rose-600', description: 'Claim submission' },
  { id: 'Employee Registration', label: 'Employee Registration', icon: Briefcase, color: 'from-fuchsia-500 to-purple-600', description: 'HR onboarding' },
  { id: 'Student Registration', label: 'Student Registration', icon: Users, color: 'from-lime-500 to-green-600', description: 'Student enrollment' },
  { id: 'Custom Form', label: 'Custom Form', icon: Puzzle, color: 'from-slate-500 to-slate-600', description: 'Build your own form' },
]

// ─── Processing Steps ─────────────────────────────────────────────────────────
const PROCESSING_STEPS = [
  { id: 'upload', label: 'Uploading Document', icon: UploadIcon, desc: 'Saving file to server' },
  { id: 'ocr', label: 'OCR Extraction', icon: Cpu, desc: 'Reading text from document' },
  { id: 'clean', label: 'Text Cleaning', icon: Layers, desc: 'Normalizing OCR output' },
  { id: 'nlp', label: 'Entity Extraction', icon: Brain, desc: 'Identifying fields and values' },
  { id: 'map', label: 'Semantic Mapping', icon: Zap, desc: 'Matching to form fields' },
  { id: 'generate', label: 'Generating Form', icon: ClipboardList, desc: 'Building your form' },
]

// ─── Step Indicator ───────────────────────────────────────────────────────────
function StepIndicator({ currentStep }: { currentStep: number }) {
  const steps = ['Select Form', 'Upload', 'Processing', 'Review & Submit']
  return (
    <div className="flex items-center justify-center gap-0 mb-8">
      {steps.map((label, i) => {
        const stepNum = i + 1
        const isActive = stepNum === currentStep
        const isDone = stepNum < currentStep
        return (
          <div key={i} className="flex items-center">
            <div className="flex flex-col items-center">
              <motion.div
                animate={{
                  scale: isActive ? 1.1 : 1,
                  backgroundColor: isDone ? '#6d28d9' : isActive ? '#8b5cf6' : '#1e293b'
                }}
                className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold border-2 transition-all ${
                  isDone ? 'border-violet-500 text-white'
                  : isActive ? 'border-violet-400 text-white shadow-lg shadow-violet-500/30'
                  : 'border-slate-700 text-slate-500'
                }`}
              >
                {isDone ? <CheckCircle size={14} /> : stepNum}
              </motion.div>
              <span className={`mt-1.5 text-[10px] font-semibold whitespace-nowrap ${
                isActive ? 'text-violet-300' : isDone ? 'text-violet-500' : 'text-slate-600'
              }`}>{label}</span>
            </div>
            {i < steps.length - 1 && (
              <div className={`w-16 h-0.5 mx-2 mb-5 transition-colors ${
                stepNum < currentStep ? 'bg-violet-600' : 'bg-slate-800'
              }`} />
            )}
          </div>
        )
      })}
    </div>
  )
}

// ─── Main Upload Wizard ───────────────────────────────────────────────────────
export default function Upload() {
  const navigate = useNavigate()

  // Wizard state
  const [step, setStep] = useState<1 | 2 | 3 | 4>(1)
  const [selectedFormType, setSelectedFormType] = useState<string | null>(null)
  const [customSchema, setCustomSchema] = useState<any>(null)

  // File state
  const [file, setFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [dragActive, setDragActive] = useState(false)
  const [uploadedFilename, setUploadedFilename] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Processing state
  const [processingStepIndex, setProcessingStepIndex] = useState(-1)
  const [processingError, setProcessingError] = useState<string | null>(null)

  // ─── File Validation ─────────────────────────────────────────────────────
  const validateFile = (f: File): string | null => {
    if (f.size > MAX_FILE_SIZE) return 'File exceeds the 20MB size limit.'
    const ext = '.' + f.name.split('.').pop()?.toLowerCase()
    if (!ALLOWED_EXTENSIONS.includes(ext)) return 'Only PDF, DOCX, JPG, JPEG, PNG files are allowed.'
    return null
  }

  const applyFile = (f: File) => {
    const err = validateFile(f)
    if (err) { toast.error(err); return }
    setFile(f)
    if (f.type.startsWith('image/')) {
      setPreviewUrl(URL.createObjectURL(f))
    } else {
      setPreviewUrl(null)
    }
  }

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setDragActive(false)
    const dropped = e.dataTransfer.files[0]
    if (dropped) applyFile(dropped)
  }, [])

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const picked = e.target.files?.[0]
    if (picked) applyFile(picked)
  }

  const clearFile = () => {
    setFile(null)
    setPreviewUrl(null)
    setUploadedFilename(null)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  // ─── Processing Pipeline ─────────────────────────────────────────────────
  const runPipeline = async () => {
    if (!file || !selectedFormType) return
    setProcessingError(null)
    setStep(3)

    try {
      // Step 0: Upload file
      setProcessingStepIndex(0)
      const formData = new FormData()
      formData.append('file', file)
      const uploadRes: any = await apiClient.post('/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      const filename = uploadRes.filename
      setUploadedFilename(filename)

      // Steps 1–5: Run full pipeline (OCR → clean → NLP → map → generate)
      for (let i = 1; i <= 5; i++) {
        setProcessingStepIndex(i)
        await new Promise(r => setTimeout(r, 400)) // visual pacing
      }

      // Call unified /process endpoint
      const processRes: any = await apiClient.post('/process', {
        filename,
        form_type: selectedFormType,
        custom_schema: selectedFormType === 'Custom Form' ? customSchema : undefined
      })

      toast.success('Form generated successfully!')

      // Navigate to review page
      navigate('/review', {
        state: {
          schema: processRes.schema,
          formData: processRes.form_data,
          autofillMap: processRes.autofill_map,
          stats: processRes.stats,
          formType: selectedFormType,
          filename: file.name,
        }
      })
    } catch (err: any) {
      const msg = err.message || 'Processing failed. Please try again.'
      setProcessingError(msg)
      toast.error(msg)
      setStep(2)
      setProcessingStepIndex(-1)
    }
  }

  // ─── STEP 1: Form Selection ───────────────────────────────────────────────
  const renderStep1 = () => (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} transition={{ duration: 0.3 }}>
      <div className="text-center mb-8">
        <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-violet-300 via-purple-200 to-white bg-clip-text text-transparent mb-2">
          Select Target Form
        </h1>
        <p className="text-slate-400 text-sm">Choose the type of form you want to fill. We'll auto-populate it from your document.</p>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
        {FORM_TYPES.map((ft) => {
          const Icon = ft.icon
          const isSelected = selectedFormType === ft.id
          return (
            <motion.button
              key={ft.id}
              onClick={() => setSelectedFormType(ft.id)}
              whileHover={{ scale: 1.03, y: -2 }}
              whileTap={{ scale: 0.97 }}
              className={`relative flex flex-col items-center p-4 rounded-2xl border-2 text-center transition-all duration-200 group ${
                isSelected
                  ? 'border-violet-500 bg-violet-950/40 shadow-lg shadow-violet-500/20'
                  : 'border-slate-800 bg-slate-900/40 hover:border-slate-700 hover:bg-slate-900/60'
              }`}
            >
              {isSelected && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute top-2 right-2 w-5 h-5 bg-violet-500 rounded-full flex items-center justify-center"
                >
                  <CheckCircle size={12} className="text-white" />
                </motion.div>
              )}
              <div className={`w-11 h-11 rounded-xl bg-gradient-to-br ${ft.color} flex items-center justify-center mb-3 shadow-md group-hover:shadow-lg transition-shadow`}>
                <Icon size={20} className="text-white" />
              </div>
              <span className={`text-xs font-bold leading-tight mb-1 ${isSelected ? 'text-violet-200' : 'text-slate-200'}`}>
                {ft.label}
              </span>
              <span className="text-[10px] text-slate-500 leading-tight">{ft.description}</span>
            </motion.button>
          )
        })}
      </div>

      {/* Custom Form Builder */}
      <AnimatePresence>
        {selectedFormType === 'Custom Form' && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-6 overflow-hidden"
          >
            <CustomFormBuilder onChange={setCustomSchema} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Next button */}
      <div className="mt-8 flex justify-end">
        <motion.button
          disabled={!selectedFormType || (selectedFormType === 'Custom Form' && !customSchema?.sections?.length)}
          onClick={() => setStep(2)}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="flex items-center gap-2.5 px-7 py-3 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 text-white font-bold rounded-2xl shadow-lg shadow-violet-500/25 disabled:opacity-40 disabled:cursor-not-allowed disabled:shadow-none transition-all"
        >
          Continue to Upload
          <ChevronRight size={18} />
        </motion.button>
      </div>
    </motion.div>
  )

  // ─── STEP 2: Upload Document ──────────────────────────────────────────────
  const renderStep2 = () => {
    const ft = FORM_TYPES.find(f => f.id === selectedFormType)
    const Icon = ft?.icon || FileText

    return (
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} transition={{ duration: 0.3 }}>
        <div className="text-center mb-8">
          <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r ${ft?.color || 'from-violet-500 to-purple-600'} text-white text-sm font-bold mb-4 shadow-lg`}>
            <Icon size={14} />
            {selectedFormType}
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-violet-300 via-purple-200 to-white bg-clip-text text-transparent mb-2">
            Upload Your Document
          </h1>
          <p className="text-slate-400 text-sm">Upload a PDF, DOCX, JPG, JPEG, or PNG. Our AI will extract and auto-fill the form.</p>
        </div>

        {/* Drop Zone */}
        <div
          onDragOver={(e) => { e.preventDefault(); setDragActive(true) }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
          onClick={() => !file && fileInputRef.current?.click()}
          className={`relative border-2 border-dashed rounded-3xl transition-all duration-300 ${
            dragActive
              ? 'border-violet-500 bg-violet-950/20 scale-[1.01]'
              : file
              ? 'border-emerald-600/50 bg-emerald-950/10 cursor-default'
              : 'border-slate-700 bg-slate-900/20 hover:border-violet-700/50 hover:bg-violet-950/10 cursor-pointer'
          }`}
          style={{ minHeight: '280px' }}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept={ALLOWED_MIME_TYPES.join(',')}
            onChange={handleFileInput}
            className="hidden"
          />

          {file ? (
            <div className="flex flex-col items-center justify-center h-full p-8 gap-5">
              {previewUrl ? (
                <img src={previewUrl} alt="Preview" className="max-h-40 max-w-xs rounded-xl shadow-lg object-contain border border-slate-700" />
              ) : (
                <div className="w-20 h-20 bg-gradient-to-br from-violet-600 to-purple-700 rounded-2xl flex items-center justify-center shadow-xl">
                  <FileText size={36} className="text-white" />
                </div>
              )}
              <div className="text-center">
                <p className="font-bold text-slate-100 text-base">{file.name}</p>
                <p className="text-sm text-slate-400 mt-1">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={(e) => { e.stopPropagation(); clearFile() }}
                  className="flex items-center gap-2 px-4 py-2 text-xs font-semibold text-rose-400 bg-rose-950/20 border border-rose-900/40 rounded-xl hover:bg-rose-950/40 transition-colors"
                >
                  <X size={13} /> Remove
                </button>
                <button
                  onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click() }}
                  className="flex items-center gap-2 px-4 py-2 text-xs font-semibold text-slate-300 bg-slate-900 border border-slate-800 rounded-xl hover:bg-slate-800 transition-colors"
                >
                  <UploadIcon size={13} /> Change File
                </button>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-full p-10 gap-4 pointer-events-none" style={{ minHeight: '280px' }}>
              <motion.div
                animate={{ y: [0, -8, 0] }}
                transition={{ repeat: Infinity, duration: 2.5, ease: 'easeInOut' }}
                className="w-20 h-20 bg-gradient-to-br from-slate-800 to-slate-900 border-2 border-slate-700 rounded-2xl flex items-center justify-center"
              >
                <UploadIcon size={32} className="text-violet-400" />
              </motion.div>
              <div className="text-center">
                <p className="text-slate-200 font-semibold">Drag & drop your file here</p>
                <p className="text-slate-500 text-sm mt-1">or <span className="text-violet-400 font-semibold">click to browse</span></p>
              </div>
              <div className="flex items-center gap-2 flex-wrap justify-center">
                {['PDF', 'DOCX', 'JPG', 'JPEG', 'PNG'].map(ext => (
                  <span key={ext} className="text-[10px] font-bold text-slate-500 bg-slate-900 border border-slate-800 px-2.5 py-1 rounded-lg">{ext}</span>
                ))}
                <span className="text-[10px] text-slate-600 ml-1">Max 20MB</span>
              </div>
            </div>
          )}
        </div>

        {/* Navigation */}
        <div className="mt-6 flex items-center justify-between">
          <button
            onClick={() => setStep(1)}
            className="flex items-center gap-2 px-5 py-2.5 text-sm font-semibold text-slate-400 bg-slate-900 border border-slate-800 rounded-2xl hover:bg-slate-800 hover:text-slate-200 transition-colors"
          >
            <ChevronLeft size={16} /> Back
          </button>

          <motion.button
            disabled={!file}
            onClick={runPipeline}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="flex items-center gap-2.5 px-7 py-3 bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-500 hover:to-purple-500 text-white font-bold rounded-2xl shadow-lg shadow-violet-500/25 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
          >
            Process Document
            <ArrowRight size={18} />
          </motion.button>
        </div>
      </motion.div>
    )
  }

  // ─── STEP 3: Processing ───────────────────────────────────────────────────
  const renderStep3 = () => (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} className="max-w-lg mx-auto">
      <div className="text-center mb-10">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ repeat: Infinity, duration: 2, ease: 'linear' }}
          className="inline-block mb-4"
        >
          <Loader2 size={40} className="text-violet-400" />
        </motion.div>
        <h1 className="text-2xl font-extrabold tracking-tight text-white mb-2">Processing Your Document</h1>
        <p className="text-slate-400 text-sm">Please wait while our AI extracts and maps the information.</p>
      </div>

      {processingError && (
        <div className="mb-6 p-4 bg-rose-950/30 border border-rose-800/50 rounded-2xl flex items-start gap-3">
          <AlertTriangle size={18} className="text-rose-400 mt-0.5 flex-shrink-0" />
          <div>
            <p className="text-rose-300 font-semibold text-sm">Processing Failed</p>
            <p className="text-rose-400 text-xs mt-1">{processingError}</p>
          </div>
        </div>
      )}

      <div className="space-y-3">
        {PROCESSING_STEPS.map((s, i) => {
          const Icon = s.icon
          const isDone = processingStepIndex > i
          const isActive = processingStepIndex === i
          return (
            <motion.div
              key={s.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: i <= processingStepIndex ? 1 : 0.35, x: 0 }}
              transition={{ delay: i * 0.08 }}
              className={`flex items-center gap-4 p-4 rounded-2xl border transition-all ${
                isDone ? 'bg-emerald-950/20 border-emerald-800/40'
                : isActive ? 'bg-violet-950/30 border-violet-700/50 shadow-lg shadow-violet-500/10'
                : 'bg-slate-900/30 border-slate-800/50'
              }`}
            >
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${
                isDone ? 'bg-emerald-600'
                : isActive ? 'bg-violet-600'
                : 'bg-slate-800'
              }`}>
                {isDone
                  ? <CheckCheck size={18} className="text-white" />
                  : isActive
                  ? <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 1.2, ease: 'linear' }}>
                      <Loader2 size={18} className="text-white" />
                    </motion.div>
                  : <Icon size={18} className="text-slate-500" />
                }
              </div>
              <div className="flex-1 min-w-0">
                <p className={`text-sm font-bold ${isDone ? 'text-emerald-300' : isActive ? 'text-violet-200' : 'text-slate-500'}`}>{s.label}</p>
                <p className={`text-xs ${isActive ? 'text-violet-400' : 'text-slate-600'}`}>{s.desc}</p>
              </div>
              {isDone && (
                <motion.span initial={{ scale: 0 }} animate={{ scale: 1 }} className="text-[10px] font-bold text-emerald-400 bg-emerald-950/40 px-2.5 py-1 rounded-full border border-emerald-800/40">
                  Done
                </motion.span>
              )}
              {isActive && (
                <motion.span animate={{ opacity: [1, 0.4, 1] }} transition={{ repeat: Infinity, duration: 1.2 }} className="text-[10px] font-bold text-violet-400 bg-violet-950/40 px-2.5 py-1 rounded-full border border-violet-700/40">
                  Running...
                </motion.span>
              )}
            </motion.div>
          )
        })}
      </div>
    </motion.div>
  )

  // ─── Render ───────────────────────────────────────────────────────────────
  return (
    <div className="space-y-2 py-4">
      <StepIndicator currentStep={step} />
      <div className="max-w-5xl mx-auto">
        <AnimatePresence mode="wait">
          {step === 1 && <div key="step1">{renderStep1()}</div>}
          {step === 2 && <div key="step2">{renderStep2()}</div>}
          {step === 3 && <div key="step3">{renderStep3()}</div>}
        </AnimatePresence>
      </div>
    </div>
  )
}
