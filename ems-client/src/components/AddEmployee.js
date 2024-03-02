import React, { useState, useEffect } from "react";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import axios from 'axios';
import { Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

export default function AddEmployee(props) {
    const [firstName, setFirstName ] = useState("");
    const [middleName, setMiddleName ] = useState("");
    const [lastName, setLastName ] = useState("");
    const [phoneNumber, setPhoneNumber ] = useState("");
    const [departmentId, setDepartmentId] = useState("");
    const [projectID, setProjectID] = useState("");
    const [managerName, setManagerName] = useState("");
    const [position, setPosition] = useState("")
    const [bankAccountNumber, setBankAccountNumber] = useState("")
    const [bankIFSCCode, setBankIFSCCode] = useState("");
    const [bankName, setBankName] = useState("");
    const [error, setError] = useState(null);
    const [departmentList, setDepartmentList] = useState([])
    const [positionList, setPositionList] = useState([])


    const [otp, setOTP] = useState(null);
    const [otpSent, setOTPSent] = useState(false);
    const [phoneNumVerified, setPhoneNumVerified] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const access_token = localStorage.getItem("access_token");
    

        axios.get('http://localhost:5000/admin/departments', { headers: { "Authorization": `Bearer ${access_token}` } })
        .then(res => {
            
            const data = res.data;
            console.log("Departments", data.department_list);
            setDepartmentList(data.department_list);
            
        })
        .catch((err) => { console.log(err.response); });
        axios.get('http://localhost:5000/admin/positions', { headers: { "Authorization": `Bearer ${access_token}` } })
        .then(res => {
            
            const data = res.data;
            console.log("Positions", data.position_list);
            setPositionList(data.position_list);
            
        })
        .catch((err) => { console.log(err.response); });
        
    }, []);

    useEffect(() => {
        if(otp){
            console.log(otp);
            const access_token = localStorage.getItem("access_token");
            axios.post(`http://localhost:5000/auth/check_verification`, 
            {
                phone_number: `+91${phoneNumber}`, 
                otp: otp
            }, 
            { 
                headers: { "Authorization": `Bearer ${access_token}` }
            }
            )
            .then(res => {
            
            const data = res.data;
            console.log("Verification STEP 2", data);
            if(data.verified){
                setError("OTP verified");
                setPhoneNumVerified(true);
            }else{
                setError("wrong otp! try again");
                setOTP(null);
            }
            
        })
        .catch((err) => { 
            console.log(err.response); 
            setOTPSent(false);
            setOTP(null);
        });
        }
            
    }, [otp])

    const handleFirstNameChange = (event) => {
        setFirstName(event.target.value);
    };
    const handleMiddleNameChange = (event) => {
        setMiddleName(event.target.value);
    };
    const handleLastNameChange = (event) => {
        setLastName(event.target.value);
    };
    const handlePhoneNumberChange = (event) => {
        setPhoneNumber(event.target.value);
        setPhoneNumVerified(false);
    };

    const handleDepartmentChange = (event) => {
        setDepartmentId(event.target.value);
    }

    const handleProjectIDChange = (event) => {
        setProjectID(event.target.value);
    }

    const handlePositionChange = (event) => {
        setPosition(event.target.value);
    }

    const handleBankAccountNumberChange = (event) => {
        setBankAccountNumber(event.target.value);
    }
    const handleBankIFSCNumberChange = (event) => {
        setBankIFSCCode(event.target.value);
    }

    const handleBankNameChange = (event) => {
        setBankName(event.target.value);
    }
    const getManagerName = (event) => {
        console.log("event called");
        const access_token = localStorage.getItem("access_token");

        axios.get(`http://localhost:5000/admin/project_manager/${projectID}`, { headers: { "Authorization": `Bearer ${access_token}` } })
        .then(res => {
            
            const data = res.data;
            console.log("Manager", data);
            if(data.manager_name)
                setManagerName(data.manager_name);
            else
                setManagerName("No such project");
            
        })
        .catch((err) => { console.log(err.response); });
    }
    const verifyPhoneNumber = (event) => {

        if(otpSent && !otp) {
            const OTP = prompt("Enter OTP");
            if(OTP)
                setOTP(OTP);
            return;
        }


            
        const access_token = localStorage.getItem("access_token");
        console.log(phoneNumber, `Bearer ${access_token}`);
        

        axios.post(`http://localhost:5000/auth/verify_phone`,            
            {
                phone_number: `+91${phoneNumber}`
            }, 
            { 
                headers: { "Authorization": `Bearer ${access_token}` }
            }
        )
        .then(res => {
            
            const data = res.data;
            console.log("Verification STEP 1", data);
            setOTPSent(true);
            const OTP = prompt("Enter OTP");
            if(OTP)
                setOTP(OTP);
            
        })
        .catch((err) => { console.log(err.response); });

    }
    const handleFormSubmit = (event) => {
        event.preventDefault();
        if(!phoneNumVerified)
            return;
        const employeeData = {
            first_name: firstName, 
            middle_name: middleName, 
            last_name: lastName, 
            phone_number: phoneNumber, 
            bank_account_number: bankAccountNumber, 
            bank_name: bankName, 
            bank_IFSC_code: bankIFSCCode, 
            department_id: departmentId, 
            project_id: projectID, 
            position: position
        }
        const access_token = localStorage.getItem("access_token");
        axios.post(`http://localhost:5000/admin/add`,            
            {
                first_name: firstName, 
                middle_name: middleName, 
                last_name: lastName, 
                phone_number: `+91${phoneNumber}`, 
                bank_account_number: bankAccountNumber, 
                bank_name: bankName, 
                bank_ifsc_code: bankIFSCCode, 
                department_id: departmentId, 
                project_id: projectID, 
                position: position, 
                role_id: 'regular'
            }, 
            { 
                headers: { "Authorization": `Bearer ${access_token}` }
            }
        ).then(res => {
            const data = res.data;
            console.log(data);
            navigate("/admin");
        }).catch(err => console.log(err));

    }

    let departmentListMenuItems = departmentList.map(mItem => {
        return (
            <MenuItem value={mItem.department_id}>{mItem.name}</MenuItem>
        );
    });
    let positionListMenuItems = positionList.map(mItem => {
        return (
            <MenuItem value={mItem.position_code}>{mItem.position} </MenuItem>
        );
    });


    return (
    <Box>
        <Typography variant="h3">Add employee</Typography>
        <Typography variant="h4">{error ? error: ""}</Typography>
      <form onSubmit={handleFormSubmit}>
        <Grid container spacing={1} xs={9} style={{ margin: "20px auto" }}>
          <Grid item xs={4}>
            <TextField type="text" label="First name" fullWidth value={firstName} onChange={handleFirstNameChange} />
          </Grid>
          <Grid item xs={4}>
            <TextField type="text" label="Middle name" fullWidth value={middleName} onChange={handleMiddleNameChange} />
          </Grid>
          <Grid item xs={4}>
            <TextField type="text" label="Last name" fullWidth value={lastName} onChange={handleLastNameChange} />
          </Grid>

          <Grid item xs={6}>
            <TextField type="number" label="Contact number with country code" fullWidth value={phoneNumber} onChange={handlePhoneNumberChange}/>
          </Grid>
          <Grid item xs={2}>
              <Button onClick={verifyPhoneNumber} fullWidth color="primary" variant="contained">Verify</Button>
          </Grid>
          <Grid item xs={4}>
            <FormControl fullWidth>
              <InputLabel id="demo-simple-select-label">Department</InputLabel>
              <Select value={departmentId} label="Department" onChange={handleDepartmentChange}>
                <MenuItem value={null}>None</MenuItem>
                { departmentListMenuItems }
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={6}>
            <TextField type="number" label="Project ID" fullWidth value={projectID} onChange={handleProjectIDChange} onBlur={getManagerName}/>
          </Grid>
          <Grid item xs={6}>
            <TextField label="Manager name" fullWidth disabled value={managerName}/>
          </Grid>
          <Grid item xs={12}>
            <FormControl fullWidth>
              <InputLabel id="demo-simple-select-label">Position</InputLabel>
              <Select value={position} label="Position" onChange={handlePositionChange}>
                { positionListMenuItems }

              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={4}>
            <TextField label="Bank account number" fullWidth onChange={handleBankAccountNumberChange} value={bankAccountNumber} />
          </Grid>
          <Grid item xs={4}>
            <TextField label="Bank IFSC code" fullWidth onChange={handleBankIFSCNumberChange} value={bankIFSCCode} />
          </Grid>
          <Grid item xs={4}>
            <TextField label="Bank name" fullWidth onChange={handleBankNameChange} value={bankName}/>
          </Grid>

          <Grid item xs={12}>
              <Button color="primary" variant="contained" type="submit" fullWidth>Add employee</Button>
          </Grid>

        </Grid>
      </form>
    </Box>
  );
}
