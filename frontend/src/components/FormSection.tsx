import React from 'react'
import { motion } from 'framer-motion'
import { 
  User, 
  Mail, 
  GraduationCap, 
  Briefcase, 
  Fingerprint,
  LucideIcon
} from 'lucide-react'

// Map key names to standard Lucide icons
const ICON_MAP: Record<string, LucideIcon> = {
  personal_information: User,
  contact_information: Mail,
  education: GraduationCap,
  professional: Briefcase,
  identification: Fingerprint
}

interface FormSectionProps {
  id: string
  title: string
  children: React.ReactNode
}

export default function FormSection({ id, title, children }: FormSectionProps) {
  // Resolve icon
  const IconComponent = ICON_MAP[id] || User

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -15 }}
      transition={{ duration: 0.3 }}
      className="bg-slate-900/30 backdrop-blur-md border border-slate-800/80 rounded-3xl p-6 shadow-xl relative overflow-hidden"
    >
      {/* Decorative top glass border */}
      <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-slate-700/30 to-transparent" />

      {/* Section Header */}
      <div className="flex items-center space-x-3 border-b border-slate-800/60 pb-4 mb-5">
        <div className="p-2 bg-brand-500/10 border border-brand-500/20 text-brand-400 rounded-xl">
          <IconComponent size={20} />
        </div>
        <h2 className="text-lg font-bold tracking-tight text-slate-100 bg-gradient-to-r from-slate-100 to-slate-300 bg-clip-text text-transparent">
          {title}
        </h2>
      </div>

      {/* Children Fields Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {children}
      </div>
    </motion.div>
  )
}
