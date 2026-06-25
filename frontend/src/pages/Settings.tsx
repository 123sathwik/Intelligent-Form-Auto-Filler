import React from 'react'

export default function Settings() {
  return (
    <div>
      <h1 className="text-3xl font-black bg-gradient-to-r from-brand-300 via-indigo-200 to-white bg-clip-text text-transparent">
        System Settings
      </h1>
      <p className="mt-2 text-slate-400">
        Configure OCR mapping thresholds, integrations, and ML parameters.
      </p>
      <div className="mt-8 space-y-6 max-w-xl">
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h3 className="font-bold text-slate-200">Integration Configuration</h3>
          <p className="text-xs text-slate-500 mt-1">Configure external data synchronization endpoints.</p>
        </div>
      </div>
    </div>
  )
}
