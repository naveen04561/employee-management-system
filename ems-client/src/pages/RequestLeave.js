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
import { adminListItems, mainListItems } from '../components/ListItems';
import Button from '@mui/material/Button';
import { useNavigate } from "react-router-dom";
import LogoutIcon from '@mui/icons-material/Logout';
import axios from 'axios';
import { Grid, TextField } from '@mui/material';

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

function RequestLeaveContent() {
    const [open, setOpen] = React.useState(true);
    const [employee, setEmployee] = useState({});
    let navigate = useNavigate();
    const toggleDrawer = () => {
        setOpen(!open);
    };

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
        getEmployeeDetails();
    }, []);

    const logout = () => {
        localStorage.clear();
        navigate('/');
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        var startDate = data.get('startDate')
        startDate = startDate.substring(8) + '-' + startDate.substring(5, 8) + startDate.substring(0, 4);
        var endDate = data.get('endDate');
        endDate = endDate.substring(8) + '-' + endDate.substring(5, 8) + endDate.substring(0, 4);
        const reason = data.get('reason');
        console.log(startDate);
        console.log(endDate);
        console.log(reason);
        const formData = new FormData();
        formData.append('start_date', startDate);
        formData.append('end_date', endDate);
        formData.append('reason', reason);
        const access_token = localStorage.getItem("access_token");
        if (startDate != null && endDate != null && reason.length > 0) {
            axios.post('http://localhost:5000/employees/apply_leave', formData, { headers: { "Authorization": `Bearer ${access_token}` } })
                .then(res => {
                    alert("Leave Request Submitted Successfullly. Refresh to see changes")
                })
                .catch((err) => { alert(err.response.data); })
        } else {
            alert("Please enter valid start date, end date and reason")
        }
    };

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
                        {employee && employee.role_id === "regular" && mainListItems}
                        {employee && employee.role_id === "admin" && adminListItems}
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
                            Request for Leave
                        </Typography>
                        <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
                            <Grid container spacing={2}>
                                <Grid item xs={12} sm={6}>
                                    <label>Start Date: </label>
                                    <input type="date" id="startDate" name="startDate" required />
                                </Grid>
                                <Grid item xs={12} sm={6}>
                                    <label>End Date: </label>
                                    <input type="date" id="endDate" name="endDate" required />
                                </Grid>
                                <Grid item xs={12}>
                                    <TextField
                                        required
                                        fullWidth
                                        id="reason"
                                        label="Reason"
                                        name="reason"
                                    />
                                </Grid>
                            </Grid>
                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                sx={{ mt: 3, mb: 2 }}
                            >
                                Submit Leave Request
                            </Button>
                        </Box>
                    </Box>
                </Box>
            </Box>
        </ThemeProvider>
    );
}

export default function RequestLeave() {
    return <RequestLeaveContent />;
}