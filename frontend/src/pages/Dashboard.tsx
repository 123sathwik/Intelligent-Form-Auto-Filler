import React from 'react'

export default function Dashboard() {
  return (
    <div>
      <h1 className="text-3xl font-black bg-gradient-to-r from-brand-300 via-indigo-200 to-white bg-clip-text text-transparent">
        System Overview
      </h1>
      <p className="mt-2 text-slate-400">
        Welcome to your intelligent form auto-filler dashboard.
      </p>
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h3 className="font-bold text-slate-200">Processed Files</h3>
          <p className="text-4xl font-extrabold text-brand-400 mt-2">0</p>
        </div>
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h3 className="font-bold text-slate-200">Active Mappings</h3>
          <p className="text-4xl font-extrabold text-indigo-400 mt-2">0</p>
        </div>
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
          <h3 className="font-bold text-slate-200">Accuracy Rate</h3>
          <p className="text-4xl font-extrabold text-emerald-400 mt-2">0%</p>
        </div>
      </div>
    </div>
  )
}
