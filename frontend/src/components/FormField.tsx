import React from 'react'
import { RotateCcw } from 'lucide-react'

// Helper to auto-detect input type based on JSON key and current value
export function detectFieldType(key: string, value: any): 'text' | 'textarea' | 'dropdown' | 'date' | 'checkbox' | 'number' | 'email' | 'phone' {
  if (typeof value === 'boolean') return 'checkbox'
  
  const keyLower = key.toLowerCase()
  
  if (keyLower.includes('email') || keyLower.includes('mail')) {
    return 'email'
  }
  if (keyLower.includes('phone') || keyLower.includes('mobile') || keyLower.includes('contact') || keyLower.includes('tel')) {
    return 'phone'
  }
  if (keyLower.includes('dob') || keyLower.includes('date') || keyLower.includes('birthday')) {
    return 'date'
  }
  if (keyLower.includes('age') || keyLower.includes('cgpa') || keyLower.includes('percentage') || keyLower.includes('pincode') || typeof value === 'number') {
    return 'number'
  }
  if (keyLower.includes('gender') || keyLower.includes('sex')) {
    return 'dropdown'
  }
  if (
    keyLower.includes('address') || 
    keyLower.includes('experience') || 
    keyLower.includes('project') || 
    keyLower.includes('description') ||
    keyLower.includes('skills') ||
    keyLower.includes('certificates') ||
    (value && typeof value === 'string' && value.length > 50)
  ) {
    return 'textarea'
  }
  
  return 'text'
}

// Helper to perform quick validation mapping
export function validateField(key: string, value: any, required: boolean = false): string | null {
  const strVal = String(value === undefined || value === null ? '' : value).trim()
  
  if (required && !strVal) {
    return 'This field is required'
  }
  
  if (!strVal) return null
  
  const type = detectFieldType(key, value)
  
  if (type === 'email') {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(strVal)) {
      return 'Please enter a valid email address'
    }
  }
  
  if (type === 'phone') {
    const phoneDigits = strVal.replace(/\D/g, '')
    if (phoneDigits.length < 10) {
      return 'Please enter a valid phone number (at least 10 digits)'
    }
  }
  
  if (type === 'date') {
    const timestamp = Date.parse(strVal)
    if (isNaN(timestamp)) {
      return 'Please enter a valid date (YYYY-MM-DD)'
    }
  }
  
  if (type === 'number') {
    const num = Number(strVal)
    if (isNaN(num)) {
      return 'Please enter a valid number'
    }
  }
  
  return null
}

interface FormFieldProps {
  name: string
  label: string
  value: any
  originalValue: any
  required?: boolean
  error?: string | null
  onChange: (val: any) => void
  onUndoField?: () => void
}

export default function FormField({
  name,
  label,
  value,
  originalValue,
  required = false,
  error = null,
  onChange,
  onUndoField
}: FormFieldProps) {
  // 1. Auto-detect input type
  const type = detectFieldType(name, value)
  
  // 2. Determine if field has been modified from its original JSON state
  const isModified = String(value) !== String(originalValue)
  
  // 3. Setup standard styles
  const baseInputStyle = `w-full bg-slate-950 text-slate-100 placeholder-slate-600 px-4 py-2.5 rounded-xl border transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-brand-500/20 ${
    error
      ? 'border-rose-500 focus:border-rose-500'
      : isModified
      ? 'border-violet-500 focus:border-violet-500 shadow-[0_0_8px_rgba(139,92,246,0.1)]'
      : 'border-slate-800 focus:border-brand-500'
  }`

  // Render components
  return (
    <div className="space-y-1.5 flex flex-col w-full relative group">
      <div className="flex justify-between items-center text-xs">
        <label className="text-slate-400 font-bold tracking-wide">
          {label}
          {required && <span className="text-rose-500 ml-1 font-black">*</span>}
        </label>
        
        {isModified && (
          <div className="flex items-center space-x-2 animate-fade-in">
            <span className="text-[10px] font-bold text-violet-400 bg-violet-950/40 border border-violet-900 px-1.5 py-0.5 rounded-md select-none">
              Modified
            </span>
            {onUndoField && (
              <button
                type="button"
                onClick={onUndoField}
                title="Undo changes to this field"
                className="text-slate-500 hover:text-slate-300 transition-colors p-0.5 hover:bg-slate-800 rounded-md"
              >
                <RotateCcw size={12} />
              </button>
            )}
          </div>
        )}
      </div>

      {type === 'checkbox' ? (
        <div className="flex items-center space-x-3 py-2">
          <input
            id={name}
            type="checkbox"
            checked={!!value}
            onChange={(e) => onChange(e.target.checked)}
            className="w-5 h-5 rounded-lg bg-slate-950 border-slate-800 text-brand-600 focus:ring-brand-500/20 focus:ring-2"
          />
          <span className="text-sm text-slate-300">Enabled</span>
        </div>
      ) : type === 'textarea' ? (
        <textarea
          id={name}
          value={value === null || value === undefined ? '' : String(value)}
          onChange={(e) => onChange(e.target.value)}
          rows={3}
          className={`${baseInputStyle} resize-y text-sm leading-relaxed`}
          placeholder={`Enter ${label.toLowerCase()}...`}
        />
      ) : type === 'dropdown' ? (
        <select
          id={name}
          value={value === null || value === undefined ? '' : String(value)}
          onChange={(e) => onChange(e.target.value)}
          className={`${baseInputStyle} text-sm`}
        >
          <option value="" disabled className="bg-slate-950">Select gender...</option>
          <option value="Male" className="bg-slate-950">Male</option>
          <option value="Female" className="bg-slate-950">Female</option>
          <option value="Other" className="bg-slate-950">Other</option>
        </select>
      ) : (
        <input
          id={name}
          type={type === 'number' ? 'text' : type} // text allows cleaner values like cgpa decimals
          value={value === null || value === undefined ? '' : String(value)}
          onChange={(e) => onChange(e.target.value)}
          className={`${baseInputStyle} text-sm`}
          placeholder={`Enter ${label.toLowerCase()}...`}
        />
      )}

      {error && (
        <span className="text-xs text-rose-500 font-semibold animate-slide-in">
          {error}
        </span>
      )}
    </div>
  )
}
