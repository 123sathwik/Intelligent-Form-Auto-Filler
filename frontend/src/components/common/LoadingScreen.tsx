import React from 'react'
import { motion } from 'framer-motion'

export default function LoadingScreen() {
  return (
    <div className="fixed inset-0 flex flex-col items-center justify-center bg-slate-950 text-white z-50">
      <motion.div
        className="w-16 h-16 border-4 border-brand-500 border-t-transparent rounded-full"
        animate={{ rotate: 360 }}
        transition={{
          repeat: Infinity,
          duration: 1,
          ease: 'linear',
        }}
      />
      <motion.p
        className="mt-6 text-sm font-semibold tracking-widest text-slate-400 uppercase"
        initial={{ opacity: 0.3 }}
        animate={{ opacity: 1 }}
        transition={{
          repeat: Infinity,
          duration: 1.5,
          repeatType: 'reverse',
        }}
      >
        Loading System Environment...
      </motion.p>
    </div>
  )
}
