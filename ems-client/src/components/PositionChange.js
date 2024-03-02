import * as React from "react";
import Box from "@mui/material/Box";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Divider from "@mui/material/Divider";
import InboxIcon from "@mui/icons-material/Inbox";
import DraftsIcon from "@mui/icons-material/Drafts";
import CircularProgress from '@mui/material/CircularProgress';

import {
  Modal,
  Typography,
  Grid,
  TextField,
  Select,
  MenuItem,
  Button
} from "@mui/material";
import EmojiEventsSharpIcon from "@mui/icons-material/EmojiEventsSharp";
import { useState, useEffect } from "react";
import axios from "axios";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: "40%",
  minWidth: "500px",
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4
};

export default function PositionChange() {
  const [open, toggleOpen] = useState(false);
  const [currentPosition, setCurrentPosition] = useState("");
  const [recommendedFor, setRecommendedFor] = useState(null);
  const [empId, setEmpId] = useState(null);
  const [empName, setEmpName] = useState("");
  const [statusPromotion, setStatusPromotion] = useState(null);
  const [reason, setReason] = useState("");
  const [recommendedBy, setRecommendedBy] = useState("");
  const [recommendedById, setRecommendedById] = useState("");
  const [promotionId, setPromotionId] = useState(null);
  const [promotionRecommendationList, setPromotionRecommendationList] = useState([])
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDetails = () => {
        const access_token = localStorage.getItem("access_token");
        axios.get(`http://localhost:5000/admin/change_position`, { headers: { "Authorization": `Bearer ${access_token}` } })
        .then(res => {
            
            const data = res.data;
            console.log("Manager", data.recommendation_list);
            console.log("Promotions", promotionRecommendationList);
            setPromotionRecommendationList(data.recommendation_list);
        })
        .catch((err) => { console.log(err.response); });
    }
    fetchDetails();
    setInterval(fetchDetails, 30000);
  }, []);
  const handlePositionChange = (event) => {
    setRecommendedFor(event.target.value);
  };
  const handleClose = () => {
    setLoading(true);
    setEmpName("");
    setCurrentPosition("");
    setRecommendedBy("");
    setRecommendedById("");

    toggleOpen(false);
  };
  const handleOpen = (promotionInfo) => (event) => {
    setEmpId(promotionInfo.employee_id);
    setPromotionId(promotionInfo.promotion_id);
    setReason(promotionInfo.reason);
    setRecommendedFor(promotionInfo.recommended_for);
    setStatusPromotion(promotionInfo.status);
    const access_token = localStorage.getItem("access_token");
    axios
      .get(`http://localhost:5000/admin/edit/${promotionInfo.employee_id}`, {
        headers: { Authorization: `Bearer ${access_token}` },
      })
      .then((res) => {
        const data = res.data;
        console.log("Existing employee details", data);
        setEmpName(`${data.f_name} ${data.m_name} ${data.l_name}`);
        setCurrentPosition(data.position);
        return axios
        .get(`http://localhost:5000/admin/edit/${promotionInfo.recommended_by}`, {
          headers: { Authorization: `Bearer ${access_token}` },
        });
        

      }).then((res) => {
        const data = res.data;
        console.log("Manager details", data);
        setRecommendedBy(`${data.f_name} ${data.m_name} ${data.l_name}`);
        setRecommendedById(data.employee_id);
        setLoading(false);
      })
      .catch((err) => {
        console.log(err.response, "NO SUCH EMPLOYEE");

      });
      
    toggleOpen(true);
  };

  const handleFormSubmit = (event) => {
      event.preventDefault();
      const confirmation = window.confirm(
        "Are you sure you want to promote this employee ?"
      );
      if (!confirmation) return;
        const access_token = localStorage.getItem("access_token");
  
      axios
        .post(
          `http://localhost:5000/admin/change_position`,
          {
            employee_id: empId, 
            recommended_by: recommendedById, 
            recommended_for: recommendedFor
          },
          {
            headers: { Authorization: `Bearer ${access_token}` },
          }
        )
        .then((res) => {
            setLoading(true);
            setEmpName("");
            setCurrentPosition("");
            setRecommendedBy("");
        
            toggleOpen(false);
          // navigate("");
        })
        .catch((err) => {
            console.log(err);
            
          });
  }

  let promotionItemsList = promotionRecommendationList.map(pItem => {
      console.log("Promotion id", pItem);
      return (
        
        <ListItem key={pItem.promotion_id}>
        <ListItemButton onClick={handleOpen(pItem)}>
          <ListItemIcon>
            <EmojiEventsSharpIcon />
          </ListItemIcon>
          <ListItemText
            primary={`Request ID - ${pItem.promotion_id}`}
            secondary={`Recommended for - ${pItem.recommended_for}`}
          />
        </ListItemButton>
      </ListItem>
      
      )
  });

  return (
    <Box sx={{ width: "100%", maxWidth: "100%", bgcolor: "background.paper" }}>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
          <Typography
            sx={{ margin: "10px auto" }}
            id="modal-modal-title"
            variant="h6"
            component="h2"
          >
            Change employee position
          </Typography>
          <Divider />
          <Grid container spacing={2} margin="10px auto">
            <form onSubmit={handleFormSubmit}>
            <Grid item xs={8}>
              <TextField
                type="number"
                disabled
                label="Employee ID"
                value={empId} 
                fullWidth
              />
            </Grid>
            <Grid item xs={8}>
              <TextField
                type="text"
                disabled
                label="Promotion ID"
                value={promotionId} 
                fullWidth
              />
            </Grid>
            <Grid item xs={8}>
              <TextField
                type="text"
                disabled
                label="Reason for promotion"
                value={reason} rows={3} 
                fullWidth
              />
            </Grid>
            <Grid item xs={8}>
              <TextField
                type="text"
                disabled
                label="Recommended By"
                value={recommendedBy} 
                fullWidth
              />
            </Grid>
            <Grid item xs={2}>
                {loading ? <CircularProgress />: ""}
            </Grid>
            <Grid item xs={10}>
              <TextField
                type="text"
                disabled
                label="Employee Name"
                value={empName}
                fullWidth
              />
            </Grid>
            <Grid item xs={2}>
                {loading ? <CircularProgress />: ""}
            </Grid>
            <Grid item xs={8}>
              <TextField
                type="text"
                disabled
                label="Employee current position"
                value={currentPosition}
                fullWidth
              />
            </Grid>
            <Grid item xs={2}>
                {loading ? <CircularProgress />: ""}
            </Grid>
            <Grid item xs={8}>
                <TextField
                type="text"
                disabled
                label="Recommended for"
                value={recommendedFor} 
                fullWidth
              />
            </Grid>
            <Grid item xs={10}>
              <TextField
                type="text"
                disabled
                label="Status"
                value={statusPromotion} 
                fullWidth
              />
            </Grid>
            <Grid item xs={8}>
              <Button type="submit" variant="contained" color="secondary">
                Change Position
              </Button>
            </Grid>
            </form>
          </Grid>
        </Box>
      </Modal>
      <nav aria-label="main mailbox folders">
        <List>
            {promotionItemsList}
          
        </List>
      </nav>
      <Divider />
    </Box>
  );
}
