import React, { useState, useEffect } from "react";
import Grid from "@mui/material/Grid";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import axios from "axios";
import { Typography, Alert, AlertTitle } from "@mui/material";
import { useNavigate } from "react-router-dom";

export default function TerminateEmployee(props) {
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [empId, setEmpId] = useState(null);
  const [employee, setEmployee] = useState(null);

  const handleEmpIdChange = (event) => {
    setEmpId(event.target.value);
    setSuccess(null);
    setError(null);
  };
  const getEmployeeDetails = (event) => {
    const access_token = localStorage.getItem("access_token");
    if (!empId) return;
    axios
      .get(`http://localhost:5000/admin/edit/${empId}`, {
        headers: { Authorization: `Bearer ${access_token}` },
      })
      .then((res) => {
        const data = res.data;
        console.log("Existing employee details", data);
        setEmployee(data);
        setError(null);
      })
      .catch((err) => {
        console.log(err.response, "NO SUCH EMPLOYEE");
        setEmployee(null);
        setError("No such employee")
      });
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();
    // return;
    if (!empId) return;

    const confirmation = window.confirm(
      "Are you sure you want to terminate this employee ?"
    );
    if (!confirmation) return;
    const access_token = localStorage.getItem("access_token");

    axios
      .post(
        `http://localhost:5000/admin/terminate`,
        {
          employee_id: empId,
        },
        {
          headers: { Authorization: `Bearer ${access_token}` },
        }
      )
      .then((res) => {
        const data = res.data;
        console.log(data);
        setEmpId("");
        setEmployee(null);
        setError(null);
        setSuccess("Successfully terminated employee");
        // navigate("");
      })
      .catch((err) => {
          console.log(err);
          setError("Failed to terminate employee.. Try again later");
        });
  };

  return (
    <Box margin="20px auto">
      <Typography variant="h4">Terminate employee</Typography>
      <Grid container spacing={1}>
        <Grid item xs={8}>
          {error ? (
            <Alert severity="error" margin="20px auto">
              <AlertTitle>Error</AlertTitle>
                {error}
            </Alert>
          ) : (
            ""
          )}
        </Grid>
        <Grid item xs={8}>
          {success ? (
            <Alert severity="success" margin="20px auto">
              <AlertTitle>Success</AlertTitle>
                {success}
            </Alert>
          ) : (
            ""
          )}
        </Grid>
      </Grid>
      <form onSubmit={handleFormSubmit}>
        <Grid container spacing={1}>
          <Grid item xs={8}>
            <TextField
              type="number"
              label="Employee ID"
              value={empId}
              fullWidth
              onChange={handleEmpIdChange}
              onBlur={getEmployeeDetails}
            />
          </Grid>
          <Grid item xs={8}>
            <TextField
              type="text"
              label="Employee name"
              value={
                employee
                  ? `${employee.f_name} ${employee.m_name} ${employee.l_name}`
                  : ""
              }
              fullWidth
              disabled
            />
          </Grid>
          <Grid item xs={6}>
            <Button type="submit" variant="contained" color="primary">
              Terminate employee
            </Button>
          </Grid>
        </Grid>
      </form>
    </Box>
  );
}
