import React from 'react'
import FormSection from './FormSection'
import FormField from './FormField'

// Helper to format labels from snake_case key strings
export function formatLabel(key: string): string {
  const SPECIAL_MAP: Record<string, string> = {
    dob: 'Date of Birth',
    cgpa: 'CGPA',
    pan_number: 'PAN Number',
    aadhaar_number: 'Aadhaar Number',
    passport_number: 'Passport Number',
    visa_number: 'Visa Number',
    driving_license: 'Driving License',
    email: 'Email Address',
    pincode: 'Pincode / ZIP'
  }
  
  if (SPECIAL_MAP[key.toLowerCase()]) return SPECIAL_MAP[key.toLowerCase()]
  
  return key
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

interface FormRendererProps {
  formData: any
  originalData: any
  errors: Record<string, string | null>
  onFieldChange: (section: string, field: string, val: any) => void
  onUndoField: (section: string, field: string) => void
}

export default function FormRenderer({
  formData,
  originalData,
  errors,
  onFieldChange,
  onUndoField
}: FormRendererProps) {
  // Detect top-level objects as sections
  const sections = Object.keys(formData).filter(
    key => typeof formData[key] === 'object' && formData[key] !== null && !Array.isArray(formData[key])
  )
  
  return (
    <div className="space-y-6">
      {sections.map((sectionKey) => {
        const sectionData = formData[sectionKey]
        const sectionOriginal = originalData[sectionKey] || {}
        const fields = Object.keys(sectionData)
        
        return (
          <FormSection 
            key={sectionKey} 
            id={sectionKey} 
            title={formatLabel(sectionKey)}
          >
            {fields.map((fieldKey) => {
              const val = sectionData[fieldKey]
              const origVal = sectionOriginal[fieldKey]
              const errorKey = `${sectionKey}.${fieldKey}`
              const error = errors[errorKey]
              
              // Handle list/array fields (e.g. skills: ['React', 'CSS']) by stringifying them with commas
              const isArray = Array.isArray(val)
              const displayVal = isArray ? val.join(', ') : val
              const displayOrigVal = Array.isArray(origVal) ? origVal.join(', ') : origVal
              
              const handleValueChange = (newVal: any) => {
                if (isArray) {
                  const arr = String(newVal)
                    .split(',')
                    .map(item => item.trim())
                    .filter(item => item.length > 0)
                  onFieldChange(sectionKey, fieldKey, arr)
                } else {
                  onFieldChange(sectionKey, fieldKey, newVal)
                }
              }
              
              return (
                <FormField
                  key={fieldKey}
                  name={fieldKey}
                  label={formatLabel(fieldKey)}
                  value={displayVal}
                  originalValue={displayOrigVal}
                  error={error}
                  required={fieldKey === 'name' || fieldKey === 'email'}
                  onChange={handleValueChange}
                  onUndoField={() => onUndoField(sectionKey, fieldKey)}
                />
              )
            })}
          </FormSection>
        )
      })}
    </div>
  )
}
