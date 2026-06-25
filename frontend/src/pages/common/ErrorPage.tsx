import React from 'react'
import { useRouteError, Link } from 'react-router-dom'

interface RouteError {
  statusText?: string
  message?: string
}

export default function ErrorPage() {
  const error = useRouteError() as RouteError
  // eslint-disable-next-line no-console
  console.error(error)

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-950 text-white p-6">
      <div className="text-center max-w-md">
        <h1 className="text-6xl font-black text-rose-500">Oops!</h1>
        <h2 className="mt-4 text-2xl font-bold">Something went wrong</h2>
        <p className="mt-2 text-slate-400">
          An unexpected error has occurred in the application view rendering.
        </p>
        <p className="mt-4 p-4 rounded-lg bg-slate-900 border border-slate-800 text-sm font-mono text-rose-400 break-all">
          {error.statusText || error.message || 'Unknown error'}
        </p>
        <div className="mt-6">
          <Link
            to="/"
            className="inline-flex items-center px-4 py-2 text-sm font-semibold rounded-lg bg-brand-600 hover:bg-brand-500 text-white transition-colors"
          >
            Return to Dashboard
          </Link>
        </div>
      </div>
    </div>
  )
}
