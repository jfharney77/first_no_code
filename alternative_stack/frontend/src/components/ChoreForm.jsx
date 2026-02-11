import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { getChore, createChore, updateChore, getTeamMembers } from '../api'

export default function ChoreForm() {
    const { id, date: prefillDate } = useParams()
    const navigate = useNavigate()
    const isEdit = !!id

    const [form, setForm] = useState({ title: '', description: '', date: prefillDate || '', assigned_to: '' })
    const [members, setMembers] = useState([])
    const [error, setError] = useState(null)

    useEffect(() => {
        getTeamMembers().then(setMembers)
        if (isEdit) {
            getChore(id).then(c => setForm({
                title: c.title,
                description: c.description,
                date: c.date,
                assigned_to: c.assigned_to ?? '',
            }))
        }
    }, [id])

    const handleSubmit = async (e) => {
        e.preventDefault()
        const payload = {
            ...form,
            assigned_to: form.assigned_to === '' ? null : parseInt(form.assigned_to),
        }
        try {
            if (isEdit) {
                await updateChore(id, payload)
                navigate(`/chore/${id}`)
            } else {
                await createChore(payload)
                navigate('/')
            }
        } catch (err) {
            setError(err.message)
        }
    }

    const change = (field) => (e) => setForm({ ...form, [field]: e.target.value })

    return (
        <>
            <h2>{isEdit ? 'Edit' : 'Add'} Chore</h2>
            {error && <div className="alert alert-danger">{error}</div>}

            <form onSubmit={handleSubmit} className="mt-3" style={{ maxWidth: 500 }}>
                <div className="mb-3">
                    <label className="form-label">Title</label>
                    <input className="form-control" value={form.title} onChange={change('title')} required />
                </div>
                <div className="mb-3">
                    <label className="form-label">Description</label>
                    <textarea className="form-control" rows={3} value={form.description} onChange={change('description')} />
                </div>
                <div className="mb-3">
                    <label className="form-label">Date</label>
                    <input type="date" className="form-control" value={form.date} onChange={change('date')} required />
                </div>
                <div className="mb-3">
                    <label className="form-label">Assigned To</label>
                    <select className="form-select" value={form.assigned_to} onChange={change('assigned_to')}>
                        <option value="">Unassigned</option>
                        {members.map(m => (
                            <option key={m.id} value={m.id}>{m.name}</option>
                        ))}
                    </select>
                </div>
                <button type="submit" className="btn btn-primary">Save</button>{' '}
                {isEdit
                    ? <Link to={`/chore/${id}`} className="btn btn-secondary">Cancel</Link>
                    : <Link to="/" className="btn btn-secondary">Cancel</Link>
                }
            </form>
        </>
    )
}
