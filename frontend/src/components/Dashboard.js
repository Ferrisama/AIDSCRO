import React, { useState } from "react";
import { Grid, Paper, TextField, Button, Typography } from "@mui/material";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import axios from "axios";

const Dashboard = () => {
  const [city, setCity] = useState("");
  const [predictions, setPredictions] = useState(null);
  const [mapCenter, setMapCenter] = useState([51.505, -0.09]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("/api/predict", { city });
      setPredictions(response.data);
      // Update map center based on the first prediction
      if (response.data && response.data.length > 0) {
        setMapCenter([response.data[0].lat, response.data[0].lon]);
      }
    } catch (error) {
      console.error("Error fetching predictions:", error);
    }
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h4">AIDSCRO Dashboard</Typography>
      </Grid>
      <Grid item xs={12} md={4}>
        <Paper style={{ padding: "1rem" }}>
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="City"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              margin="normal"
            />
            <Button type="submit" variant="contained" color="primary">
              Get Predictions
            </Button>
          </form>
          {predictions && (
            <div>
              <Typography variant="h6">Predictions:</Typography>
              <pre>{JSON.stringify(predictions, null, 2)}</pre>
            </div>
          )}
        </Paper>
      </Grid>
      <Grid item xs={12} md={8}>
        <Paper style={{ height: "400px" }}>
          <MapContainer
            center={mapCenter}
            zoom={13}
            style={{ height: "100%", width: "100%" }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            />
            {predictions &&
              predictions.map((pred, index) => (
                <Marker key={index} position={[pred.lat, pred.lon]}>
                  <Popup>Jam Factor: {pred.jam_factor}</Popup>
                </Marker>
              ))}
          </MapContainer>
        </Paper>
      </Grid>
    </Grid>
  );
};

export default Dashboard;
