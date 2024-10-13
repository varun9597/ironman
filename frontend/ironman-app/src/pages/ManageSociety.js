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
} from '@mui/material'; // Import MUI components
import VisibilityIcon from '@mui/icons-material/Visibility'; // Import icons
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import '../styles/ManageSociety.css'

function ManageSociety() {
  const location = useLocation();
  const [societyData, setSocietyData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
        // Sort society data in ascending order
        const sortedData = response.data.data.sort();
        setSocietyData(sortedData); // Store societies in state
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, []);

  const handleView = (society) => {
    console.log(`View ${society}`);
    // Implement view logic
  };

  const handleEdit = (society) => {
    console.log(`Edit ${society}`);
    // Implement edit logic
  };

  const handleDelete = (society) => {
    console.log(`Delete ${society}`);
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
                  <TableRow key={society}>
                    <TableCell>{society}</TableCell> {/* Display society name */}
                    <TableCell align="right">
                      {/* View, Edit, Delete Buttons */}
                      <IconButton onClick={() => handleView(society)}>
                        <VisibilityIcon />
                      </IconButton>
                      <IconButton onClick={() => handleEdit(society)}>
                        <EditIcon />
                      </IconButton>
                      <IconButton onClick={() => handleDelete(society)}>
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </div>
    </div>
  );
}

export default ManageSociety;
