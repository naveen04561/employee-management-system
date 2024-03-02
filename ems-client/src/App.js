import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import './App.css';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import RequestLeave from "./pages/RequestLeave";
import Admin from './pages/Admin';
import AddEmployee from "./components/AddEmployee";
import EditEmployee from "./components/EditEmployee";

import Typography from "@mui/material/Typography";
import TerminateEmployee from "./components/TerminateEmployee";
import PositionChange from "./components/PositionChange";

import RaiseTicket from "./pages/RaiseTicket";
import ViewLeaveRequests from "./pages/ViewLeaveRequests";
import RecommendForPromotion from "./pages/RecommendForPromotion";
import AssignProject from "./pages/AssignProject";
import ViewExpenditure from "./pages/ViewExpenditure";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route
            path="/"
            element={
              <Login />
            }
          />
          <Route path="/dashboard" exact element={<Dashboard />} />
          <Route path="/requestLeave" exact element={<RequestLeave />} />
          <Route path="/raiseTicket" exact element={<RaiseTicket />} />
          <Route path="/viewLeaveRequests" exact element={<ViewLeaveRequests />} />
          <Route path="/recommendForPromotion" exact element={<RecommendForPromotion />} />
          <Route path="/assignProject" exact element={<AssignProject />} />
          <Route path="/viewExpenditure" exact element={<ViewExpenditure />} />
          <Route path="admin" element={<Admin />} >
            <Route path="" element={<><Typography variant="h2">Welcome to ADMIN page</Typography></>}/>
            <Route path="add" element={<AddEmployee />}/>
            <Route path="edit" element={<EditEmployee />}/>
            <Route path="terminate" element={<TerminateEmployee />} />
            <Route path="position-change" element={<PositionChange />} />
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;