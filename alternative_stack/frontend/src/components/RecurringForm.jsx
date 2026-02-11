import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { getRecurringChore, createRecurringChore, updateRecurringChore, getTeamMembers } from '../api'

export default function RecurringForm() {
    const { id } = useParams()
    const navigate = useNavigate()
    const isEdit = !!id

    const [form, setForm] = useState({
        title: '', description: '', assigned_to: '',
        start_date: '', end_date: '', is_active: true,
    })
    const [members, setMembers] = useState([])
    const [error, setError] = useState(null)

    useEffect(() => {
        getTeamMembers().then(setMembers)
        if (isEdit) {
            getRecurringChore(id).then(rc => setForm({
                title: rc.title,
                description: rc.description,
                assigned_to: rc.assigned_to ?? '',
                start_date: rc.start_date,
                end_date: rc.end_date || '',
                is_active: rc.is_active,
            }))
        }
    }, [id])

    const handleSubmit = async (e) => {
        e.preventDefault()
        const payload = {
            ...form,
            assigned_to: form.assigned_to === '' ? null : parseInt(form.assigned_to),
            end_date: form.end_date || null,
        }
        try {
            if (isEdit) {
                await updateRecurringChore(id, payload)
            } else {
                await createRecurringChore(payload)
            }
            navigate('/recurring')
        } catch (err) {
            setError(err.message)
        }
    }

    const change = (field) => (e) => setForm({ ...form, [field]: e.target.value })

    return (
        <>
            <h2>{isEdit ? 'Edit' : 'Add'} Recurring Chore</h2>
            <p className="text-muted">Recurring chores are generated biweekly (every 14 days) from the start date.</p>
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
                    <label className="form-label">Assigned To</label>
                    <select className="form-select" value={form.assigned_to} onChange={change('assigned_to')}>
                        <option value="">Unassigned</option>
                        {members.map(m => (
                            <option key={m.id} value={m.id}>{m.name}</option>
                        ))}
                    </select>
                </div>
                <div className="mb-3">
                    <label className="form-label">Start Date</label>
                    <input type="date" className="form-control" value={form.start_date} onChange={change('start_date')} required />
                </div>
                <div className="mb-3">
                    <label className="form-label">End Date (leave blank for indefinite)</label>
                    <input type="date" className="form-control" value={form.end_date} onChange={change('end_date')} />
                </div>
                <div className="mb-3 form-check">
                    <input
                        type="checkbox"
                        className="form-check-input"
                        id="is_active"
                        checked={form.is_active}
                        onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
                    />
                    <label className="form-check-label" htmlFor="is_active">Active</label>
                </div>
                <button type="submit" className="btn btn-primary">Save</button>{' '}
                <Link to="/recurring" className="btn btn-secondary">Cancel</Link>
            </form>
        </>
    )
}
