import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getRecurringChores, deleteRecurringChore, generateRecurring } from '../api'

export default function RecurringList() {
    const [recurring, setRecurring] = useState([])
    const [message, setMessage] = useState(null)

    const load = () => getRecurringChores().then(setRecurring)

    useEffect(() => { load() }, [])

    const handleDelete = async (id, title) => {
        if (!confirm(`Delete recurring rule "${title}"? Existing instances will be kept.`)) return
        await deleteRecurringChore(id)
        load()
    }

    const handleGenerate = async (id) => {
        const result = await generateRecurring(id)
        setMessage(`${result.generated} new instances generated.`)
        setTimeout(() => setMessage(null), 3000)
    }

    return (
        <>
            <div className="d-flex justify-content-between align-items-center mb-3">
                <h2>Recurring Chores</h2>
                <Link to="/recurring/add" className="btn btn-primary">Add Recurring Chore</Link>
            </div>

            {message && <div className="alert alert-success">{message}</div>}

            {recurring.length > 0 ? (
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Assigned To</th>
                            <th>Start Date</th>
                            <th>End Date</th>
                            <th>Active</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {recurring.map(rc => (
                            <tr key={rc.id}>
                                <td>{rc.title}</td>
                                <td>{rc.assigned_member ? rc.assigned_member.name : 'Unassigned'}</td>
                                <td>{rc.start_date}</td>
                                <td>{rc.end_date || 'Indefinite'}</td>
                                <td>
                                    {rc.is_active
                                        ? <span className="badge bg-success">Active</span>
                                        : <span className="badge bg-secondary">Inactive</span>
                                    }
                                </td>
                                <td>
                                    <button onClick={() => handleGenerate(rc.id)} className="btn btn-sm btn-outline-success">Generate</button>{' '}
                                    <Link to={`/recurring/${rc.id}/edit`} className="btn btn-sm btn-outline-primary">Edit</Link>{' '}
                                    <button onClick={() => handleDelete(rc.id, rc.title)} className="btn btn-sm btn-outline-danger">Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p className="text-muted">No recurring chores set up yet.</p>
            )}
        </>
    )
}
