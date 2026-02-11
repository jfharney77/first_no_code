import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { getTeamMembers, deleteTeamMember } from '../api'

export default function TeamList() {
    const [members, setMembers] = useState([])

    const load = () => getTeamMembers().then(setMembers)

    useEffect(() => { load() }, [])

    const handleDelete = async (id, name) => {
        if (!confirm(`Delete ${name}?`)) return
        await deleteTeamMember(id)
        load()
    }

    return (
        <>
            <div className="d-flex justify-content-between align-items-center mb-3">
                <h2>Team Members</h2>
                <Link to="/team/add" className="btn btn-primary">Add Member</Link>
            </div>

            {members.length > 0 ? (
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {members.map(m => (
                            <tr key={m.id}>
                                <td>{m.name}</td>
                                <td>{m.email}</td>
                                <td>
                                    <Link to={`/team/${m.id}/edit`} className="btn btn-sm btn-outline-primary">Edit</Link>{' '}
                                    <button onClick={() => handleDelete(m.id, m.name)} className="btn btn-sm btn-outline-danger">Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p className="text-muted">No team members yet. Add one to get started.</p>
            )}
        </>
    )
}
