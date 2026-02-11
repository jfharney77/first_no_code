import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { getTeamMember, createTeamMember, updateTeamMember } from '../api'

export default function TeamForm() {
    const { id } = useParams()
    const navigate = useNavigate()
    const isEdit = !!id

    const [form, setForm] = useState({ name: '', email: '' })
    const [error, setError] = useState(null)

    useEffect(() => {
        if (isEdit) {
            getTeamMember(id).then(m => setForm({ name: m.name, email: m.email }))
        }
    }, [id])

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            if (isEdit) {
                await updateTeamMember(id, form)
            } else {
                await createTeamMember(form)
            }
            navigate('/team')
        } catch (err) {
            setError(err.message)
        }
    }

    const change = (field) => (e) => setForm({ ...form, [field]: e.target.value })

    return (
        <>
            <h2>{isEdit ? 'Edit' : 'Add'} Team Member</h2>
            {error && <div className="alert alert-danger">{error}</div>}

            <form onSubmit={handleSubmit} className="mt-3" style={{ maxWidth: 500 }}>
                <div className="mb-3">
                    <label className="form-label">Name</label>
                    <input className="form-control" value={form.name} onChange={change('name')} required />
                </div>
                <div className="mb-3">
                    <label className="form-label">Email</label>
                    <input type="email" className="form-control" value={form.email} onChange={change('email')} required />
                </div>
                <button type="submit" className="btn btn-primary">Save</button>{' '}
                <Link to="/team" className="btn btn-secondary">Cancel</Link>
            </form>
        </>
    )
}
