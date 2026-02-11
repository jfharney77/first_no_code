import { useState, useEffect } from 'react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import { getChore, deleteChore, toggleChore } from '../api'

export default function ChoreDetail() {
    const { id } = useParams()
    const navigate = useNavigate()
    const [chore, setChore] = useState(null)
    const [error, setError] = useState(null)

    const load = () => getChore(id).then(setChore).catch(e => setError(e.message))

    useEffect(() => { load() }, [id])

    const handleDelete = async () => {
        if (!confirm('Delete this chore?')) return
        await deleteChore(id)
        navigate('/')
    }

    const handleToggle = async () => {
        const updated = await toggleChore(id)
        setChore(updated)
    }

    if (error) return <div className="alert alert-danger">{error}</div>
    if (!chore) return <p>Loading...</p>

    return (
        <>
            <div className="d-flex justify-content-between align-items-start mb-3">
                <h2>{chore.title}</h2>
                <div>
                    <button
                        onClick={handleToggle}
                        className={`btn btn-sm ${chore.is_completed ? 'btn-outline-secondary' : 'btn-success'}`}
                    >
                        {chore.is_completed ? 'Mark Incomplete' : 'Mark Complete'}
                    </button>{' '}
                    <Link to={`/chore/${id}/edit`} className="btn btn-sm btn-outline-primary">Edit</Link>{' '}
                    <button onClick={handleDelete} className="btn btn-sm btn-outline-danger">Delete</button>
                </div>
            </div>

            <table className="table" style={{ maxWidth: 500 }}>
                <tbody>
                    <tr>
                        <th>Date</th>
                        <td>{chore.date}</td>
                    </tr>
                    <tr>
                        <th>Assigned To</th>
                        <td>{chore.assigned_member ? chore.assigned_member.name : 'Unassigned'}</td>
                    </tr>
                    <tr>
                        <th>Status</th>
                        <td>
                            {chore.is_completed
                                ? <span className="badge bg-success">Completed</span>
                                : <span className="badge bg-warning text-dark">Pending</span>
                            }
                        </td>
                    </tr>
                    {chore.recurring_source && (
                        <tr>
                            <th>Recurring</th>
                            <td>From recurring rule #{chore.recurring_source}</td>
                        </tr>
                    )}
                </tbody>
            </table>

            {chore.description && (
                <>
                    <h5>Description</h5>
                    <p>{chore.description}</p>
                </>
            )}

            <Link to="/" className="btn btn-secondary btn-sm">Back to Calendar</Link>
        </>
    )
}
