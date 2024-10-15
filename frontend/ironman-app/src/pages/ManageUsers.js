import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import axiosInstance from "../utils/axiosInstance"; // Import Axios instance
import HeaderBar from "../components/HeaderBar/HeaderBar"; // Import HeaderBar
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
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material"; // Import MUI components
import VisibilityIcon from "@mui/icons-material/Visibility"; // Import icons
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import AddIcon from "@mui/icons-material/Add"; // Import Add Icon
import "../styles/ManageUsers.css";

function ManageUsers() {
  const location = useLocation();
  const [userData, setUserData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [editUserId, setEditUserId] = useState(null);
  const [editName, setEditName] = useState("");
  //   const [editUserName, setEditUserName] = useState('');
  const [previousName, setPreviousName] = useState(""); // Store previous name
  const [editUsername, setEditUsername] = useState(""); // State for username in edit dialog
  const [editRole, setEditRole] = useState("");
  const [openEditDialog, setOpenEditDialog] = useState(false);

  const [viewUserId, setViewUserId] = useState(null); // State for view user id
  const [viewName, setViewName] = useState(""); // State for User name in view dialog
  const [viewUsername, setViewUsername] = useState(""); // State for username in view dialog
  const [viewRole, setViewRole] = useState("");
  const [openViewDialog, setOpenViewDialog] = useState(false); // State for view dialog

    const [openDeleteDialog, setOpenDeleteDialog] = useState(false); // State for delete confirmation dialog
    const [deleteUserId, setDeleteUserId] = useState(null); // State to track which user to delete

    const [openAddDialog, setOpenAddDialog] = useState(false); // State for add user dialog
    const [newUserName, setNewUserName] = useState(''); // State to track new user name
    const [newUserRole, setNewUserRole] = useState(''); // State to track new user name
    const [newUserUsername, setNewUserUsername] = useState(''); // State to track new user name
    const [addError, setAddError] = useState(''); // State to track error when adding society

  const [resetPasswordSuccess, setResetPasswordSuccess] = useState(false); // State to track password reset status

  useEffect(() => {
    const token = sessionStorage.getItem("access_token");
    // Fetch society list from API
    axiosInstance
      .get("/fetch_user_list", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        setUserData(response.data.data); // Store societies in state
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, []);

  const handleView = (userId) => {
    axiosInstance
      .get(`/view_user/${userId}`)
      .then((response) => {
        const { name, username, role } = response.data.data;
        setViewName(name);
        setViewUsername(username); // Fetch and set username
        setViewRole(role);
        setViewUserId(userId);
        setOpenViewDialog(true); // Open view dialog
      })
      .catch((error) => {
        console.error("Error fetching society details:", error);
      });
  };

  const handlePasswordReset = () => {
    // Call the password reset API
    axiosInstance
      .post("/reset_password", {
        user_id: editUserId, // Assuming username is used for password reset
      })
      .then((response) => {
        console.log("Password reset successful:", response);
        setResetPasswordSuccess(true); // Set success message state to true
      })
      .catch((error) => {
        console.error("Error resetting password:", error);
        setResetPasswordSuccess(false); // Handle error if needed
      });
  };

  const handleEditClick = (userId) => {
    // Fetch the details for the selected society
    axiosInstance
      .get(`/view_user/${userId}`)
      .then((response) => {
        const { name, username, role } = response.data.data;
        setEditUserId(userId);
        setEditName(name); // Populate with fetched data
        setPreviousName(name); // Store previous name
        setEditUsername(username); // Set username in edit dialog
        setEditRole(role);
        setOpenEditDialog(true); // Open edit dialog
      })
      .catch((error) => {
        console.error("Error fetching society details:", error);
      });
  };

  const handleEditSubmit = () => {
    // Submit the updated society name to the API
    axiosInstance
      .post("/edit_user", {
        user_id: editUserId,
        name: editName,
        role: editRole,
      })
      .then((response) => {
        console.log("User updated successfully:", response);

        // Re-fetch the updated society details after successful edit
        axiosInstance
          .get(`/view_user/${editUserId}`)
          .then((res) => {
            const updatedUser = res.data.data;
            setUserData((prevData) =>
              prevData.map((user) =>
                user.user_id === editUserId
                  ? { ...user, name: updatedUser.name, role: updatedUser.role }
                  : user
              )
            );
            setEditName(updatedUser.name); // Update the state for dialog box
            setPreviousName(updatedUser.name); // Update the previous name
            setOpenEditDialog(false); // Close the dialog
          })
          .catch((error) => {
            console.error("Error fetching updated user details:", error);
          });
      })
      .catch((error) => {
        console.error("Error updating user:", error);
      });
  };

    const handleDeleteClick = (userId) => {
      // Open the delete confirmation dialog
      setDeleteUserId(userId);
      setOpenDeleteDialog(true);
    };

    const handleDeleteConfirm = () => {
      // Proceed with deletion once confirmed
      axiosInstance
        .post(`/delete_user`, {
          user_id: deleteUserId
        })
        .then((response) => {
          console.log('User deleted successfully:', response);

          // Remove the deleted user from the userData state
          setUserData((prevData) =>
            prevData.filter((user) => user.user_id !== deleteUserId)
          );

          // Close the delete confirmation dialog
          setOpenDeleteDialog(false);
        })
        .catch((error) => {
          console.error('Error deleting user:', error);
        });
    };

    const handleAddSubmit = () => {
      // Clear the previous error
      setAddError('');

      // Add new society via API
      axiosInstance
        .post('/add_user', {
          username: newUserUsername,
          user_name : newUserName,
          user_role : newUserRole
        })
        .then((response) => {
          console.log('User added successfully:', response);

          // Add the new user to the userData state
          setUserData((prevData) => [
            ...prevData,
            { user_id: response.data.user_id, name: newUserName, role: newUserRole },
          ]);

          setNewUserName(''); // Clear the input field
          setNewUserUsername('');
          setNewUserRole('');
          setOpenAddDialog(false); // Close the dialog
        })
        .catch((error) => {
          if (error.response || error.response.data.error === "User already exists") {
            setAddError("User with the same username already exists."); // Set error message
          } else {
            console.error('Error adding user:', error);
          }
        });
    };

  return (
    <div className="dashboard-layout">
      <HeaderBar /> {/* Add the HeaderBar at the top */}
      <div className="dash-header">
        <h2>Manage Users</h2>
        {/* Add Users Button */}
        <Button
          variant="contained"
          startIcon={<AddIcon />}
            onClick={() => setOpenAddDialog(true)} // Open add society dialog
          style={{ marginLeft: "auto" }}
        >
          Add User
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
                  <TableCell sx={{ fontWeight: "bold" }}>Username</TableCell>{" "}
                  {/* Column for society names */}
                  <TableCell sx={{ fontWeight: "bold" }}>Role</TableCell>{" "}
                  {/* Column for society names */}
                  <TableCell sx={{ fontWeight: "bold" }} align="right">
                    Actions
                  </TableCell>{" "}
                  {/* Column for actions */}
                </TableRow>
              </TableHead>
              <TableBody>
                {userData.map((user) => (
                  <TableRow key={user.user_id}>
                    <TableCell>{user.name}</TableCell>{" "}
                    {/* Display User name */}
                    <TableCell>{user.role}</TableCell>
                    <TableCell align="right">
                      <IconButton
                        onClick={() => handleView(user.user_id)} // Call handleView
                        size="small"
                        color="gray"
                      >
                        <VisibilityIcon />
                      </IconButton>
                      <IconButton
                        onClick={() => handleEditClick(user.user_id)} // Call handleEditClick
                        size="small"
                        color="gray"
                      >
                        <EditIcon />
                      </IconButton>
                      <IconButton
                        onClick={() => handleDeleteClick(user.user_id)} // Call handleDeleteClick
                        size="small"
                        color="gray"
                      >
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
      {/* View Society Dialog */}
      <Dialog open={openViewDialog} onClose={() => setOpenViewDialog(false)}>
        <DialogTitle>View User Details</DialogTitle>
        <DialogContent>
          <TextField
            margin="dense"
            label="Name"
            type="text"
            value={viewName}
            fullWidth
            InputProps={{ readOnly: true }} // Make the society name non-editable
          />
          <TextField
            margin="dense"
            label="Username"
            type="text"
            value={viewUsername} // Display the username
            fullWidth
            InputProps={{ readOnly: true }} // Make the username non-editable
          />
          <TextField
            margin="dense"
            label="Role"
            type="text"
            value={viewRole} // Display the role
            fullWidth
            InputProps={{ readOnly: true }} // Make the role non-editable
          />

          {/* Password Reset Button */}
          <Button
            variant="outlined"
            sx={{ margin: "10px" }}
            onClick={handlePasswordReset} // Call the password reset function
          >
            Reset Password
          </Button>

          {/* Show success message if password reset is successful */}
          {resetPasswordSuccess && (
            <Typography
              color="success"
              variant="body2"
              sx={{ marginTop: "10px" }}
            >
              Password reset successful!
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenViewDialog(false)}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Edit Society Dialog */}
      <Dialog open={openEditDialog} onClose={() => setOpenEditDialog(false)}>
        <DialogTitle>Edit User Details</DialogTitle>
        <DialogContent>
          <TextField
            margin="dense"
            label="Name"
            type="text"
            value={editName}
            fullWidth
            onChange={(e) => setEditName(e.target.value)} // Update editName state
          />
          <TextField
            margin="dense"
            label="Username"
            type="text"
            value={editUsername}
            fullWidth
            InputProps={{ readOnly: true }} // Make the username non-editable
          />

          {/* Dropdown for Role Selection with Label */}
          <FormControl fullWidth margin="dense">
            <InputLabel id="role-select-label">Role</InputLabel>
            <Select
              labelId="role-select-label"
              id="role-select"
              value={editRole}
              label="Role"
              onChange={(e) => setEditRole(e.target.value)} // Handle role change
            >
              <MenuItem value="resident">Resident</MenuItem>
              <MenuItem value="admin">Admin</MenuItem>
              <MenuItem value="laundry-personnel">Laundry Man</MenuItem>
            </Select>
          </FormControl>

          {/* Password Reset Button */}
          <Button
            variant="outlined"
            sx={{ margin: "10px" }}
            onClick={handlePasswordReset} // Call the password reset function
          >
            Reset Password
          </Button>

          {/* Show success message if password reset is successful */}
          {resetPasswordSuccess && (
            <Typography
              color="success"
              variant="body2"
              sx={{ marginTop: "10px" }}
            >
              Password reset successful!
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenEditDialog(false)}>Close</Button>
          <Button onClick={handleEditSubmit}>Save</Button>
        </DialogActions>
      </Dialog>

      <Dialog open={openAddDialog} onClose={() => setOpenAddDialog(false)}>
        <DialogTitle>Add New User</DialogTitle>
        <DialogContent>
          <TextField
            margin="dense"
            label="Username"
            type="text"
            value={newUserUsername}
            onChange={(e) => setNewUserUsername(e.target.value)}
            fullWidth
          />
          <TextField
            margin="dense"
            label="User Full Name"
            type="text"
            value={newUserName}
            onChange={(e) => setNewUserName(e.target.value)}
            fullWidth
          />
           <FormControl fullWidth margin="dense">
            <InputLabel id="role-select-label">Role</InputLabel>
            <Select
              labelId="role-select-label"
              id="role-select"
              value={newUserRole}
              label="Role"
              onChange={(e) => setNewUserRole(e.target.value)} // Handle role change
            >
              <MenuItem value="resident">Resident</MenuItem>
              <MenuItem value="admin">Admin</MenuItem>
              <MenuItem value="laundry-personnel">Laundry Man</MenuItem>
            </Select>
          </FormControl>
          {addError && (
            <Typography color="error" variant="body2">
              {addError}
            </Typography> // Display error if any
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAddDialog(false)}>Cancel</Button>
          <Button onClick={handleAddSubmit}>Add</Button>
        </DialogActions>
      </Dialog>

      <Dialog open={openDeleteDialog} onClose={() => setOpenDeleteDialog(false)}>
        <DialogTitle>Confirm Deletion</DialogTitle>
        <DialogContent>
          <Typography>Are you sure you want to delete this user?</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDeleteDialog(false)}>Cancel</Button>
          <Button color="secondary" onClick={handleDeleteConfirm}>Delete</Button>
        </DialogActions>
      </Dialog> 
    </div>
  );
}

export default ManageUsers;
