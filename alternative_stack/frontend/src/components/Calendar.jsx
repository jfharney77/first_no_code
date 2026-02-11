import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getCalendar } from '../api'

export default function Calendar() {
    const params = useParams()
    const now = new Date()
    const year = parseInt(params.year) || now.getFullYear()
    const month = parseInt(params.month) || now.getMonth() + 1

    const [data, setData] = useState(null)
    const [error, setError] = useState(null)

    useEffect(() => {
        getCalendar(year, month).then(setData).catch(e => setError(e.message))
    }, [year, month])

    if (error) return <div className="alert alert-danger">{error}</div>
    if (!data) return <p>Loading...</p>

    return (
        <>
            <div className="d-flex justify-content-between align-items-center mb-3">
                <Link to={`/calendar/${data.prev_year}/${data.prev_month}`} className="btn btn-outline-primary">
                    &laquo; Prev
                </Link>
                <h2 className="mb-0">{data.month_name} {data.year}</h2>
                <Link to={`/calendar/${data.next_year}/${data.next_month}`} className="btn btn-outline-primary">
                    Next &raquo;
                </Link>
            </div>

            <div className="mb-2">
                <Link to="/chore/add" className="btn btn-primary btn-sm">Add Chore</Link>
            </div>

            <table className="table table-bordered calendar-table">
                <thead className="table-primary">
                    <tr>
                        {data.day_names.map(d => (
                            <th key={d} className="text-center">{d}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data.weeks.map((week, wi) => (
                        <tr key={wi}>
                            {week.map((day) => (
                                <td
                                    key={day.date}
                                    className={`calendar-day ${!day.is_current_month ? 'calendar-other-month' : ''} ${day.is_today ? 'calendar-today' : ''}`}
                                >
                                    <div className="day-number">
                                        <Link
                                            to={`/chore/add/${day.date}`}
                                            className={day.is_today ? 'fw-bold' : ''}
                                            title={`Add chore on ${day.date}`}
                                        >
                                            {new Date(day.date + 'T00:00:00').getDate()}
                                        </Link>
                                    </div>
                                    {day.chores.map(chore => (
                                        <Link
                                            key={chore.id}
                                            to={`/chore/${chore.id}`}
                                            className={`chore-entry ${chore.is_completed ? 'chore-completed' : ''}`}
                                            title={`${chore.title}${chore.assigned_member ? ` - ${chore.assigned_member.name}` : ''}`}
                                        >
                                            {chore.title.length > 20 ? chore.title.slice(0, 17) + '...' : chore.title}
                                        </Link>
                                    ))}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </>
    )
}
