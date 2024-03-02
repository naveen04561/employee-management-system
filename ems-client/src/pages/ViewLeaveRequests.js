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
import Link from '@mui/material/Link';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import { managerListItems } from '../components/ListItems';
import Button from '@mui/material/Button';
import { useNavigate } from "react-router-dom";
import LogoutIcon from '@mui/icons-material/Logout';
import axios from 'axios';
import {
    Table, TableContainer, TableHead, TableBody, TableCell, TableRow,
    Paper, Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions
} from '@mui/material';

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

function ViewLeaveRequestsContent() {
    const [open, setOpen] = useState(true);
    const [leaves, setLeaves] = useState([]);
    const [dialogOpen, setDialogOpen] = React.useState(false);
    const [selectedLeave, setSelectedLeave] = React.useState(false);
    const [leaveState, setLeaveState] = React.useState('');
    let navigate = useNavigate();
    const toggleDrawer = () => {
        setOpen(!open);
    };

    const logout = () => {
        localStorage.clear();
        navigate('/');
    }

    const handleClickOpen = (selected_leave_id, status) => {
        setSelectedLeave(selected_leave_id)
        setDialogOpen(true);
        setLeaveState(status);
    };

    const handleClose = () => {
        setDialogOpen(false);
    };

    const handleApprove = () => {
        const access_token = localStorage.getItem("access_token");
        const formData = {leave_id: selectedLeave, leave_approval_decision: leaveState};
        axios.post('http://localhost:5000/manager/approve_leave', formData,
            { headers: { "Authorization": `Bearer ${access_token}` } })
            .then(res => {
                if(leaveState == "granted"){
                    alert("Leave Approved Successfully. Refresh to see changes")
                } else {
                    alert("Leave Disapproved Successfully. Refresh to see changes")
                }
                
            })
            .catch((err) => { alert(err.response.data); })
        setDialogOpen(false);
    };

    const getAllLeaves = function () {
        const access_token = localStorage.getItem("access_token");
        axios.get('http://localhost:5000/manager/leaves_list', { headers: { "Authorization": `Bearer ${access_token}` } })
            .then(res => {
                setLeaves(res.data.leaves_request_list);
            })
            .catch((err) => { alert(err.response.data); })
    }

    useEffect(() => {
        getAllLeaves();
    }, []);

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
                        {managerListItems}
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
                    <Box
                        sx={{
                            marginTop: 8,
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                        }}
                    >
                        <Typography component="h1" variant="h5">
                            Pending Employee Leave Requests
                        </Typography>
                        <br />
                        <TableContainer component={Paper} style={{ width: "90%" }}>
                            <Table sx={{ minWidth: 650 }} aria-label="simple table">
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Leave ID</TableCell>
                                        <TableCell>Applied Date</TableCell>
                                        <TableCell>Start Date</TableCell>
                                        <TableCell >End Date</TableCell>
                                        <TableCell >Reason</TableCell>
                                        <TableCell>Action</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {leaves.map((leave) => {
                                        return <TableRow
                                            key={leave.leave_id}
                                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                        >
                                            <TableCell component="th" scope="row">
                                                {leave.leave_id}
                                            </TableCell>
                                            <TableCell>{new Date(leave.applied_date).toLocaleDateString("en-UK")}</TableCell>
                                            <TableCell>{new Date(leave.start_date).toLocaleDateString("en-UK")}</TableCell>
                                            <TableCell>{new Date(leave.end_date).toLocaleDateString("en-UK")}</TableCell>
                                            <TableCell>{leave.reason}</TableCell>
                                            <TableCell>
                                                <Button color="success" onClick={() => handleClickOpen(leave.leave_id, 'granted')}>Approve</Button>
                                                <Button color="error" onClick={() => handleClickOpen(leave.leave_id, 'rejected')}>Disapprove</Button>
                                            </TableCell>
                                            <Dialog
                                                open={dialogOpen}
                                                onClose={handleClose}
                                                aria-labelledby="alert-dialog-title"
                                                aria-describedby="alert-dialog-description"
                                            >
                                                <DialogTitle id="alert-dialog-title">
                                                    {leaveState == 'granted' && "Are you sure you want to Approve the Leave?"}
                                                    {leaveState == 'rejected' && "Are you sure you want to Disapprove the Leave?"}
                                                </DialogTitle>
                                                <DialogContent>
                                                    <DialogContentText id="alert-dialog-description">
                                                        {leaveState == 'granted' && "By clicking on Approve, the employee's leave request will be approved by you."}
                                                        {leaveState == 'rejected' && "By clicking on Disapprove, the employee's leave request will be rejected by you."}
                                                    </DialogContentText>
                                                </DialogContent>
                                                <DialogActions>
                                                    <Button onClick={handleClose}>Cancel</Button>
                                                    {leaveState == 'granted' && <Button onClick={handleApprove} autoFocus>Approve</Button>}
                                                    {leaveState == 'rejected' && <Button onClick={handleApprove} autoFocus>Disapprove</Button>}
                                                </DialogActions>
                                            </Dialog>
                                        </TableRow>
                                    })}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </Box>
                </Box>
            </Box>
        </ThemeProvider>
    );
}

export default function ViewLeaveRequests() {
    return <ViewLeaveRequestsContent />;
}