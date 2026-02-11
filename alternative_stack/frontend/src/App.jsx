import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Calendar from './components/Calendar'
import ChoreDetail from './components/ChoreDetail'
import ChoreForm from './components/ChoreForm'
import TeamList from './components/TeamList'
import TeamForm from './components/TeamForm'
import RecurringList from './components/RecurringList'
import RecurringForm from './components/RecurringForm'

export default function App() {
    return (
        <>
            <Navbar />
            <div className="container mt-4">
                <Routes>
                    <Route path="/" element={<Calendar />} />
                    <Route path="/calendar/:year/:month" element={<Calendar />} />
                    <Route path="/chore/add" element={<ChoreForm />} />
                    <Route path="/chore/add/:date" element={<ChoreForm />} />
                    <Route path="/chore/:id" element={<ChoreDetail />} />
                    <Route path="/chore/:id/edit" element={<ChoreForm />} />
                    <Route path="/team" element={<TeamList />} />
                    <Route path="/team/add" element={<TeamForm />} />
                    <Route path="/team/:id/edit" element={<TeamForm />} />
                    <Route path="/recurring" element={<RecurringList />} />
                    <Route path="/recurring/add" element={<RecurringForm />} />
                    <Route path="/recurring/:id/edit" element={<RecurringForm />} />
                </Routes>
            </div>
        </>
    )
}
