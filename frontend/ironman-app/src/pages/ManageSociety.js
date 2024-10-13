import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance'; // Import Axios instance
import HeaderBar from '../components/HeaderBar/HeaderBar'; // Import HeaderBar
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Paper,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  Button,
} from '@mui/material'; // Import MUI components
import VisibilityIcon from '@mui/icons-material/Visibility'; // Import icons
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import '../styles/ManageSociety.css';

function ManageSociety() {
  const location = useLocation();
  const [societyData, setSocietyData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [editSocietyId, setEditSocietyId] = useState(null);
  const [editSocietyName, setEditSocietyName] = useState('');
  const [previousSocietyName, setPreviousSocietyName] = useState(''); // Store previous name
  const [openEditDialog, setOpenEditDialog] = useState(false);

  useEffect(() => {
    const token = sessionStorage.getItem('access_token');
    // Fetch society list from API
    axiosInstance
      .get('/fetch_society_list', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        setSocietyData(response.data.data); // Store societies in state
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, []);

  const handleView = (societyId) => {
    console.log(`View ${societyId}`);
    // Implement view logic
  };

  const handleEditClick = (societyId) => {
    // Fetch the details for the selected society
    axiosInstance
      .get(`/view_society/${societyId}`)
      .then((response) => {
        console.log(response.data);
        setEditSocietyId(societyId);
        setEditSocietyName(response.data.data.society_name); // Populate with fetched data
        setPreviousSocietyName(response.data.data.society_name); // Store previous name
        setOpenEditDialog(true); // Open edit dialog
      })
      .catch((error) => {
        console.error('Error fetching society details:', error);
      });
  };

  const handleEditSubmit = () => {
    // Submit the updated society name to the API
    axiosInstance
      .post('/edit_society', {
        society_id: editSocietyId,
        society_name: editSocietyName,
      })
      .then((response) => {
        console.log('Society updated successfully:', response);
        // Update the local societyData with the new name
        setSocietyData((prevData) =>
          prevData.map((society) =>
            society.society_id === editSocietyId
              ? { ...society, society_name: editSocietyName }
              : society
          )
        );
        setOpenEditDialog(false); // Close the dialog
      })
      .catch((error) => {
        console.error('Error updating society:', error);
      });
  };

  const handleDelete = (societyId) => {
    console.log(`Delete ${societyId}`);
    // Implement delete logic
  };

  return (
    <div className="dashboard-layout">
      <HeaderBar /> {/* Add the HeaderBar at the top */}

      <div className="dash-header">
        <h2>Manage Society</h2>
      </div>

      <div className="dash-content">
        {loading ? (
          <p>Loading...</p> // Show loading indicator
        ) : error ? (
          <p>Error: {error}</p> // Show error message
        ) : (
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Society Name</TableCell> {/* Column for society names */}
                  <TableCell align="right">Actions</TableCell> {/* Column for actions */}
                </TableRow>
              </TableHead>
              <TableBody>
                {societyData.map((society) => (
                  <TableRow key={society.society_id}>
                    <TableCell>{society.society_name}</TableCell> {/* Display society name */}
                    <TableCell align="right">
                      {/* View, Edit, Delete Buttons */}
                      <IconButton onClick={() => handleView(society.society_id)}>
                        <VisibilityIcon />
                      </IconButton>
                      <IconButton onClick={() => handleEditClick(society.society_id)}>
                        <EditIcon />
                      </IconButton>
                      <IconButton onClick={() => handleDelete(society.society_id)}>
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}

        {/* Edit Society Dialog */}
        <Dialog open={openEditDialog} onClose={() => setOpenEditDialog(false)}>
          <DialogTitle>Edit Society</DialogTitle>
          <DialogContent>
            {/* Show the current society name */}
            <TextField
              autoFocus
              margin="dense"
              label="Society Name"
              type="text"
              fullWidth
              value={editSocietyName}
              onChange={(e) => setEditSocietyName(e.target.value)}
              helperText={`Previous Name: ${previousSocietyName}`} // Show previous name
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenEditDialog(false)} color="primary">
              Cancel
            </Button>
            <Button onClick={handleEditSubmit} color="primary">
              Submit
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    </div>
  );
}

export default ManageSociety;
