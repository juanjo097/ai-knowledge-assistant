import * as React from 'react'
import { pipelineIngest } from '../../shared/api/endpoints'
import { useDoc } from '../../app/DocContext'

export function useUpload() {
  const { setDocId } = useDoc()
  const [busy, setBusy] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)
  const [fileName, setFileName] = React.useState<string | null>(null)

  const onFile = React.useCallback(async (file: File) => {
    setBusy(true); setError(null)
    try {
      const out = await pipelineIngest(file)
      setFileName(file.name)
      setDocId(out.doc_id)
    } catch (e: unknown) {
      if (e instanceof Error) {
        setError(e.message)
      } else {
        setError('Upload failed')
      }
    } finally {
      setBusy(false)
    }
  }, [setDocId])

  return { busy, error, fileName, onFile }
}