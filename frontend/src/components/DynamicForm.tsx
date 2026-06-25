import React, { useState, useEffect } from 'react'
import { Undo, RotateCcw, AlertCircle, Check } from 'lucide-react'
import FormRenderer from './FormRenderer'
import { validateField } from './FormField'

interface DynamicFormProps {
  initialData: any
  onJSONUpdate: (updatedJSON: any) => void
}

export default function DynamicForm({ initialData, onJSONUpdate }: DynamicFormProps) {
  // Deep clone helper
  const deepClone = (obj: any) => JSON.parse(JSON.stringify(obj))

  // 1. Form States
  const [formData, setFormData] = useState<any>(() => deepClone(initialData))
  const [originalData, setOriginalData] = useState<any>(() => deepClone(initialData))
  const [errors, setErrors] = useState<Record<string, string | null>>({})
  const [history, setHistory] = useState<any[]>([]) // Stack to support Undo
  const [modifiedCount, setModifiedCount] = useState(0)

  // Sync state if initialData changes (e.g. new file uploaded)
  useEffect(() => {
    const cloned = deepClone(initialData)
    setFormData(cloned)
    setOriginalData(cloned)
    setErrors({})
    setHistory([])
  }, [initialData])

  // 2. Count modifications
  useEffect(() => {
    let count = 0
    Object.keys(formData).forEach(sectionKey => {
      if (typeof formData[sectionKey] === 'object' && formData[sectionKey] !== null) {
        Object.keys(formData[sectionKey]).forEach(fieldKey => {
          const val = formData[sectionKey][fieldKey]
          const orig = originalData[sectionKey]?.[fieldKey]
          if (String(val) !== String(orig)) {
            count++
          }
        })
      }
    })
    setModifiedCount(count)
  }, [formData, originalData])

  // 3. Handle individual field modification
  const handleFieldChange = (sectionKey: string, fieldKey: string, newValue: any) => {
    // Save current state to history stack before making the change
    setHistory(prev => [...prev, deepClone(formData)])

    // Update form state
    const updated = deepClone(formData)
    updated[sectionKey][fieldKey] = newValue
    setFormData(updated)

    // Inline field validation check
    const isRequired = fieldKey === 'name' || fieldKey === 'email'
    const errorMsg = validateField(fieldKey, newValue, isRequired)
    
    setErrors(prev => ({
      ...prev,
      [`${sectionKey}.${fieldKey}`]: errorMsg
    }))

    // Propagate updated JSON back to parent
    onJSONUpdate(updated)
  }

  // 4. Undo a single field's changes back to its original state
  const handleUndoField = (sectionKey: string, fieldKey: string) => {
    setHistory(prev => [...prev, deepClone(formData)])

    const updated = deepClone(formData)
    updated[sectionKey][fieldKey] = deepClone(originalData[sectionKey][fieldKey])
    setFormData(updated)

    setErrors(prev => ({
      ...prev,
      [`${sectionKey}.${fieldKey}`]: null
    }))

    onJSONUpdate(updated)
  }

  // 5. Undo the last action (rollback state stack)
  const handleUndoLastAction = () => {
    if (history.length === 0) return

    const previousState = history[history.length - 1]
    setHistory(prev => prev.slice(0, -1))
    setFormData(previousState)

    // Revalidate the restored state
    const newErrors: Record<string, string | null> = {}
    Object.keys(previousState).forEach(sec => {
      if (typeof previousState[sec] === 'object' && previousState[sec] !== null) {
        Object.keys(previousState[sec]).forEach(fld => {
          const val = previousState[sec][fld]
          const req = fld === 'name' || fld === 'email'
          const err = validateField(fld, val, req)
          if (err) {
            newErrors[`${sec}.${fld}`] = err
          }
        })
      }
    })
    setErrors(newErrors)
    onJSONUpdate(previousState)
  }

  // 6. Reset all fields back to initial values
  const handleResetForm = () => {
    const restored = deepClone(originalData)
    setFormData(restored)
    setErrors({})
    setHistory([])
    onJSONUpdate(restored)
  }

  const hasErrors = Object.values(errors).some(err => err !== null)

  return (
    <div className="space-y-6">
      {/* Top Action Panel */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between p-4 bg-slate-900/40 border border-slate-800 rounded-2xl gap-3 backdrop-blur-md">
        <div className="flex items-center space-x-3">
          {modifiedCount > 0 ? (
            <span className="flex items-center text-xs font-bold text-violet-400 bg-violet-950/30 border border-violet-900/60 px-3 py-1.5 rounded-xl animate-pulse">
              <AlertCircle size={14} className="mr-1.5" />
              {modifiedCount} field{modifiedCount > 1 ? 's' : ''} modified
            </span>
          ) : (
            <span className="flex items-center text-xs font-bold text-emerald-400 bg-emerald-950/20 border border-emerald-900/40 px-3 py-1.5 rounded-xl">
              <Check size={14} className="mr-1.5" />
              Values match standard
            </span>
          )}
          
          {hasErrors && (
            <span className="flex items-center text-xs font-bold text-rose-400 bg-rose-950/20 border border-rose-900/40 px-3 py-1.5 rounded-xl">
              Contains validation errors
            </span>
          )}
        </div>

        {/* Global form controls */}
        <div className="flex items-center space-x-2.5">
          <button
            type="button"
            disabled={history.length === 0}
            onClick={handleUndoLastAction}
            className={`flex items-center justify-center px-4 py-2 text-xs font-semibold rounded-xl border transition-all duration-200 ${
              history.length === 0
                ? 'border-slate-800/50 text-slate-600 cursor-not-allowed bg-transparent'
                : 'border-slate-800 text-slate-300 bg-slate-900 hover:bg-slate-800 hover:text-slate-100'
            }`}
          >
            <Undo size={13} className="mr-1.5" />
            Undo Action
          </button>
          
          <button
            type="button"
            disabled={modifiedCount === 0}
            onClick={handleResetForm}
            className={`flex items-center justify-center px-4 py-2 text-xs font-semibold rounded-xl border transition-all duration-200 ${
              modifiedCount === 0
                ? 'border-slate-800/50 text-slate-600 cursor-not-allowed bg-transparent'
                : 'border-slate-800 text-slate-300 bg-slate-900 hover:bg-slate-800 hover:text-slate-100 hover:border-violet-500/50'
            }`}
          >
            <RotateCcw size={13} className="mr-1.5" />
            Reset Form
          </button>
        </div>
      </div>

      {/* Main Form Fields Container */}
      <FormRenderer
        formData={formData}
        originalData={originalData}
        errors={errors}
        onFieldChange={handleFieldChange}
        onUndoField={handleUndoField}
      />
    </div>
  )
}
