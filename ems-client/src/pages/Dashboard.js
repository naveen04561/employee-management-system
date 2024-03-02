import React, { useEffect, useState } from 'react';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import MuiDrawer from '@mui/material/Drawer';
import Box from '@mui/material/Box';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Link from '@mui/material/Link';
// import { MainListItems } from '../components/ListItems';
import { mainListItems, managerListItems, adminListItems, accountantListItems } from '../components/ListItems';
import { Button, Table, TableBody, TableContainer, TableHead, TableRow, TableCell, Container } from '@mui/material';
import { useNavigate } from "react-router-dom";
import LogoutIcon from '@mui/icons-material/Logout';
import axios from 'axios';

import jwt_decode from "jwt-decode";

const drawerWidth = 240;

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  zIndex: theme.zIndex.drawer + 1,
  transition: theme.transitions.create(['width', 'margin'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    '& .MuiDrawer-paper': {
      position: 'relative',
      whiteSpace: 'nowrap',
      width: drawerWidth,
      transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
      }),
      boxSizing: 'border-box',
      ...(!open && {
        overflowX: 'hidden',
        transition: theme.transitions.create('width', {
          easing: theme.transitions.easing.sharp,
          duration: theme.transitions.duration.leavingScreen,
        }),
        width: theme.spacing(7),
        [theme.breakpoints.up('sm')]: {
          width: theme.spacing(9),
        },
      }),
    },
  }),
);

const mdTheme = createTheme();

function DashboardContent() {
  const [open, setOpen] = React.useState(true);
  const [employee, setEmployee] = useState(null);
  const [role, setRole] = useState(null);
  let navigate = useNavigate();
  const toggleDrawer = () => {
    setOpen(!open);
  };

  const getEmpIdentity = () => {
    const token = localStorage.getItem("access_token");
    const res = jwt_decode(token);

    console.log(res);
    return res.sub;

  }
  const getEmployeeDetails = () => {
    const access_token = localStorage.getItem("access_token");
    axios.get('http://localhost:5000/employees/', { headers: { "Authorization": `Bearer ${access_token}` } })
      .then(res => {

        const data = res.data;
        setEmployee(data)
        console.log("Data from employees", data);

      })
      .catch((err) => { alert(err.response.data); })
  }

  useEffect(() => {
    const { role, employee_id } = getEmpIdentity();
    console.log("ROLE", role, "id", employee_id);
    setRole(role);
  }, []);
  useEffect(() => {
    getEmployeeDetails();
    setInterval(() => {
      getEmployeeDetails()
    }, 300000);
  }, []);

  const logout = () => {
    localStorage.clear();
    navigate('/');
  }

  const DetailsComponent = ({ emp }) => {
    if (emp)
      return (
        <>

          <Typography variant="h4">Personal details</Typography>

          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
              <TableBody>

                <TableRow
                  key="employeeName"
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell component="th" scope="row">Full name</TableCell>
                  <TableCell align="right">{`${emp.personal.first_name} ${emp.personal.middle_name} ${emp.personal.last_name}`}</TableCell>

                </TableRow>
                <TableRow
                  key="employeePhoneNumber"
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell component="th" scope="row">Phone number</TableCell>
                  <TableCell align="right">{emp.personal.phone_number}</TableCell>

                </TableRow>

              </TableBody>
            </Table>
          </TableContainer>
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
              <TableBody>

                <TableRow
                  key="employeeManagerName"
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell component="th" scope="row">Manager name</TableCell>
                  <TableCell align="right">{emp.manager_name != "" ? emp.manager_name : "Not assigned manager yet"}</TableCell>

                </TableRow>
                <TableRow
                  key="employeeDepartmentName"
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell component="th" scope="row">Department name</TableCell>
                  <TableCell align="right">{emp.department_name ? emp.department_name : "Not assigned department yet"}</TableCell>

                </TableRow>

              </TableBody>
            </Table>
          </TableContainer>
          <Accordion>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel1a-content"
              id="panel1a-header"
            >
              <Typography variant="h4">Bank details</Typography>

            </AccordionSummary>
            <AccordionDetails>

              <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                  <TableBody>

                    <TableRow
                      key="employeeName"
                      sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                    >
                      <TableCell component="th" scope="row">Bank Account Number</TableCell>
                      <TableCell align="right">{emp.bank_details.bank_account_num}</TableCell>

                    </TableRow>
                    <TableRow
                      key="employeePhoneNumber"
                      sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                    >
                      <TableCell component="th" scope="row">Bank IFSC code</TableCell>
                      <TableCell align="right">{emp.bank_details.bank_IFSC_code}</TableCell>

                    </TableRow>

                  </TableBody>
                </Table>
              </TableContainer>
            </AccordionDetails>
          </Accordion>


        </>
      )
  }

  return (
    <ThemeProvider theme={mdTheme}>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <AppBar position="absolute" open={open}>
          <Toolbar
            sx={{
              pr: '24px', // keep right padding when drawer closed
            }}
          >
            <IconButton
              edge="start"
              color="inherit"
              aria-label="open drawer"
              onClick={toggleDrawer}
              sx={{
                marginRight: '36px',
                ...(open && { display: 'none' }),
              }}
            >
              <MenuIcon />
            </IconButton>
            <Typography
              component="h1"
              variant="h6"
              color="inherit"
              noWrap
              sx={{ flexGrow: 1 }}
            >
              Dashboard
            </Typography>
            {/* <IconButton color="inherit">
              <Badge badgeContent={4} color="secondary">
                <NotificationsIcon />
              </Badge>
            </IconButton> */}
            <Button variant="contained" startIcon={<LogoutIcon />} style={{ color: "white" }} onClick={logout}>Logout</Button>
          </Toolbar>
        </AppBar>
        <Drawer variant="permanent" open={open}>
          <Toolbar
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'flex-end',
              px: [1],
            }}
          >
            <IconButton onClick={toggleDrawer}>
              <ChevronLeftIcon />
            </IconButton>
          </Toolbar>
          <Divider />
          <List component="nav">
            {employee && employee.role_id === "admin" && adminListItems}
            {employee && employee.role_id === "regular" && mainListItems}
            {employee && employee.role_id === "manager" && managerListItems}
            {employee && employee.role_id === "accountant" && accountantListItems}
          </List>
        </Drawer>
        <Box
          component="main"
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === 'light'
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: '100vh',
            overflow: 'auto',
          }}
        >
          <Toolbar />
          {/* Main content here */}
          <DetailsComponent emp={employee} />
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default function Dashboard() {
  return <DashboardContent />;
}