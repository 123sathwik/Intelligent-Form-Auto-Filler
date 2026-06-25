import React from 'react'
import { Link } from 'react-router-dom'
import { FileQuestion } from 'lucide-react'

export default function NotFoundPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-950 text-white p-6">
      <div className="text-center max-w-sm flex flex-col items-center">
        <div className="p-4 bg-slate-900 border border-slate-800 rounded-2xl text-brand-400">
          <FileQuestion size={48} />
        </div>
        <h1 className="mt-6 text-5xl font-black">404</h1>
        <h2 className="mt-2 text-xl font-bold">Page Not Found</h2>
        <p className="mt-2 text-slate-400 text-sm leading-relaxed">
          The link you followed may be broken, or the page may have been removed.
        </p>
        <div className="mt-6">
          <Link
            to="/"
            className="inline-flex items-center px-4 py-2 text-sm font-semibold rounded-lg bg-brand-600 hover:bg-brand-500 text-white transition-colors"
          >
            Go Back Home
          </Link>
        </div>
      </div>
    </div>
  )
}
