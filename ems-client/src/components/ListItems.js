import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import PersonIcon from '@mui/icons-material/Person';
import DirectionsWalkIcon from '@mui/icons-material/DirectionsWalk';
import ReceiptLongIcon from '@mui/icons-material/ReceiptLong';
import HistoryIcon from '@mui/icons-material/History';
import ConfirmationNumberIcon from '@mui/icons-material/ConfirmationNumber';
import AssignmentIcon from '@mui/icons-material/Assignment';
import CancelRoundedIcon from '@mui/icons-material/CancelRounded';
import EditSharpIcon from '@mui/icons-material/EditSharp';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import ManageAccountsIcon from '@mui/icons-material/ManageAccounts';
import { useNavigate } from 'react-router-dom';
import AssignmentTurnedInIcon from '@mui/icons-material/AssignmentTurnedIn';
import ListAltIcon from '@mui/icons-material/ListAlt';
import RecommendIcon from '@mui/icons-material/Recommend';
import { Link as RouterLink } from 'react-router-dom';

// export const AdminListItems = ({ role }) => {
//   const navigate = useNavigate();
  
//   console.log("MAIN LIST ITEMS");
//   if(role === "admin")
//     return (
//     <React.Fragment>
//       <ListItemButton>
//         <ListItemIcon>
//           <AddCircleIcon />
//         </ListItemIcon>
//         <ListItemText primary="Add employee" onClick={() => navigate(`add`)}/>
//       </ListItemButton>
//       <ListItemButton>
//         <ListItemIcon>
//           <EditSharpIcon />
//         </ListItemIcon>
//         <ListItemText primary="Edit employee" onClick={() => navigate(`edit`)}/>
//       </ListItemButton>
//       <ListItemButton>
//         <ListItemIcon>
//           <CancelRoundedIcon />
//         </ListItemIcon>
//         <ListItemText primary="Terminate employee" onClick={() => navigate('terminate')}/>
//       </ListItemButton>
//       <ListItemButton>
//         <ListItemIcon>
//           <ManageAccountsIcon />
//         </ListItemIcon>
//         <ListItemText primary="Position Change" onClick={() => navigate('position-change')} />
//       </ListItemButton>
//       <ListItemButton>
//         <ListItemIcon>
//           <ConfirmationNumberIcon />
//         </ListItemIcon>
//         <ListItemText primary="Raise Ticket" />
//       </ListItemButton>
      
//     </React.Fragment>
//   );
// }

export const mainListItems = (
  <React.Fragment>
    <ListItemButton component={RouterLink} to="/dashboard">
      <ListItemIcon>
        <PersonIcon />
      </ListItemIcon>
      <ListItemText primary="Profile" />
    </ListItemButton>
    <ListItemButton component={RouterLink} to="/requestLeave">
      <ListItemIcon>
        <DirectionsWalkIcon />
      </ListItemIcon>
      <ListItemText primary="Leave Requests" />
    </ListItemButton>
    <ListItemButton>
      <ListItemIcon>
        <ReceiptLongIcon />
      </ListItemIcon>
      <ListItemText primary="Salary Slip" />
    </ListItemButton>
    <ListItemButton>
      <ListItemIcon>
        <HistoryIcon />
      </ListItemIcon>
      <ListItemText primary="Transaction History" />
    </ListItemButton>
    <ListItemButton component={RouterLink} to="/raiseTicket">
      <ListItemIcon>
        <ConfirmationNumberIcon />
      </ListItemIcon>
      <ListItemText primary="Raise Ticket" />
    </ListItemButton>
  </React.Fragment>
);

export const adminListItems = (
  <React.Fragment>
    {mainListItems}
      <ListItemButton component={RouterLink} to="/admin/add">
        <ListItemIcon>
          <AddCircleIcon />
        </ListItemIcon>
        <ListItemText primary="Add employee"/>
      </ListItemButton>
      <ListItemButton component={RouterLink} to="/admin/edit">
        <ListItemIcon>
          <EditSharpIcon />
        </ListItemIcon>
        <ListItemText primary="Edit employee"/>
      </ListItemButton>
      <ListItemButton component={RouterLink} to="/admin/terminate">
        <ListItemIcon>
          <CancelRoundedIcon />
        </ListItemIcon>
        <ListItemText primary="Terminate employee"/>
      </ListItemButton>
      <ListItemButton component={RouterLink} to="/admin/position-change">
        <ListItemIcon>
          <ManageAccountsIcon />
        </ListItemIcon>
        <ListItemText primary="Position Change" />
      </ListItemButton>
    </React.Fragment>
);

export const managerListItems = (
  <React.Fragment>
    <ListItemButton component={RouterLink} to="/dashboard">
      <ListItemIcon>
        <PersonIcon />
      </ListItemIcon>
      <ListItemText primary="Profile" />
    </ListItemButton>
    <ListItemButton component={RouterLink} to="/assignProject">
      <ListItemIcon>
        <AssignmentTurnedInIcon />
      </ListItemIcon>
      <ListItemText primary="Assign Project" />
    </ListItemButton>
    <ListItemButton component={RouterLink} to="/recommendForPromotion">
      <ListItemIcon>
        <RecommendIcon />
      </ListItemIcon>
      <ListItemText primary="Recommend for Promotion"
      primaryTypographyProps={{ style: { whiteSpace: "normal" } }} />
    </ListItemButton>
    <ListItemButton component={RouterLink} to="/viewLeaveRequests">
      <ListItemIcon>
        <ListAltIcon />
      </ListItemIcon>
      <ListItemText primary="View Leave Requests" 
      primaryTypographyProps={{ style: { whiteSpace: "normal" } }} />
    </ListItemButton>
  </React.Fragment>
);

export const accountantListItems = (
  <React.Fragment>
    <ListItemButton component={RouterLink} to="/dashboard">
      <ListItemIcon>
        <PersonIcon />
      </ListItemIcon>
      <ListItemText primary="Profile" />
    </ListItemButton>
    <ListItemButton component={RouterLink} to="/viewExpenditure">
      <ListItemIcon>
        <AssignmentTurnedInIcon />
      </ListItemIcon>
      <ListItemText primary="View expenditure of the company"
      primaryTypographyProps={{ style: { whiteSpace: "normal" } }} />
    </ListItemButton>    
  </React.Fragment>
);