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
  Typography, // Import Typography to show error text
} from '@mui/material'; // Import MUI components
import VisibilityIcon from '@mui/icons-material/Visibility'; // Import icons
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add'; // Import Add Icon
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

  const [openDeleteDialog, setOpenDeleteDialog] = useState(false); // State for delete confirmation dialog
  const [deleteSocietyId, setDeleteSocietyId] = useState(null); // State to track which society to delete

  const [openAddDialog, setOpenAddDialog] = useState(false); // State for add society dialog
  const [newSocietyName, setNewSocietyName] = useState(''); // State to track new society name
  const [addError, setAddError] = useState(''); // State to track error when adding society

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
        
        // Re-fetch the updated society details after successful edit
        axiosInstance
          .get(`/view_society/${editSocietyId}`)
          .then((res) => {
            const updatedSociety = res.data.data;
            setSocietyData((prevData) =>
              prevData.map((society) =>
                society.society_id === editSocietyId
                  ? { ...society, society_name: updatedSociety.society_name }
                  : society
              )
            );
            setEditSocietyName(updatedSociety.society_name); // Update the state for dialog box
            setPreviousSocietyName(updatedSociety.society_name); // Update the previous name
            setOpenEditDialog(false); // Close the dialog
          })
          .catch((error) => {
            console.error('Error fetching updated society details:', error);
          });
      })
      .catch((error) => {
        console.error('Error updating society:', error);
      });
  };

  const handleDeleteClick = (societyId) => {
    // Open the delete confirmation dialog
    setDeleteSocietyId(societyId);
    setOpenDeleteDialog(true);
  };

  const handleDeleteConfirm = () => {
    // Proceed with deletion once confirmed
    axiosInstance
      .post(`/delete_society`, {
        society_id: deleteSocietyId
      })
      .then((response) => {
        console.log('Society deleted successfully:', response);

        // Remove the deleted society from the societyData state
        setSocietyData((prevData) =>
          prevData.filter((society) => society.society_id !== deleteSocietyId)
        );

        // Close the delete confirmation dialog
        setOpenDeleteDialog(false);
      })
      .catch((error) => {
        console.error('Error deleting society:', error);
      });
  };

  const handleAddSubmit = () => {
    // Clear the previous error
    setAddError('');

    // Add new society via API
    axiosInstance
      .post('/add_society', {
        society_name: newSocietyName,
      })
      .then((response) => {
        console.log('Society added successfully:', response);

        // Add the new society to the societyData state
        setSocietyData((prevData) => [
          ...prevData,
          { society_id: response.data.society_id, society_name: newSocietyName },
        ]);

        setNewSocietyName(''); // Clear the input field
        setOpenAddDialog(false); // Close the dialog
      })
      .catch((error) => {
        if (error.response || error.response.data.error === "Society already exists") {
          setAddError("Society with the same name already exists."); // Set error message
        } else {
          console.error('Error adding society:', error);
        }
      });
  };

  return (
    <div className="dashboard-layout">
      <HeaderBar /> {/* Add the HeaderBar at the top */}

      <div className="dash-header">
        <h2>Manage Society</h2>
        {/* Add Society Button */}
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenAddDialog(true)} // Open add society dialog
          style={{ marginLeft: 'auto' }}
        >
          Add Society
        </Button>
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
                      <IconButton onClick={() => handleDeleteClick(society.society_id)}>
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}

        {/* Add Society Dialog */}
        <Dialog open={openAddDialog} onClose={() => setOpenAddDialog(false)}>
          <DialogTitle>Add Society</DialogTitle>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              label="Society Name"
              type="text"
              fullWidth
              value={newSocietyName}
              onChange={(e) => setNewSocietyName(e.target.value)}
            />
            {/* Display error message if society already exists */}
            {addError && (
              <Typography color="error" variant="body2">
                {addError}
              </Typography>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => {setOpenAddDialog(false); setNewSocietyName('');}}>Cancel</Button>
            <Button onClick={handleAddSubmit}>Add</Button>
          </DialogActions>
        </Dialog>

        {/* Edit Society Dialog */}
        <Dialog open={openEditDialog} onClose={() => setOpenEditDialog(false)}>
          <DialogTitle>Edit Society</DialogTitle>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              label="Society Name"
              type="text"
              fullWidth
              value={editSocietyName}
              onChange={(e) => setEditSocietyName(e.target.value)}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenEditDialog(false)}>Cancel</Button>
            <Button onClick={handleEditSubmit}>Save</Button>
          </DialogActions>
        </Dialog>

        {/* Delete Society Confirmation Dialog */}
        <Dialog open={openDeleteDialog} onClose={() => setOpenDeleteDialog(false)}>
          <DialogTitle>Confirm Delete</DialogTitle>
          <DialogContent>
            <p>Are you sure you want to delete this society?</p>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDeleteDialog(false)}>Cancel</Button>
            <Button onClick={handleDeleteConfirm}>Delete</Button>
          </DialogActions>
        </Dialog>
      </div>
    </div>
  );
}

export default ManageSociety;
