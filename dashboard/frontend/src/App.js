import React, { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceLine,
} from "recharts";
import axios from "axios";
import "./App.css";

function App() {
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [changePoints, setChangePoints] = useState([]);
  const [dateRange, setDateRange] = useState({
    start: "1987-05-20",
    end: "2022-09-30",
  });
  const [selectedEvents, setSelectedEvents] = useState([]);

  // Fetch data from FastAPI
  useEffect(() => {
    axios
      .get("http://localhost:8000/api/prices")
      .then((res) => setPrices(res.data))
      .catch((err) => console.error("Error fetching prices:", err));

    axios
      .get("http://localhost:8000/api/events")
      .then((res) => {
        setEvents(res.data);
        setSelectedEvents(res.data.map((event) => event.Event));
      })
      .catch((err) => console.error("Error fetching events:", err));

    axios
      .get("http://localhost:8000/api/change_points")
      .then((res) => setChangePoints(res.data))
      .catch((err) => console.error("Error fetching change points:", err));
  }, []);

  // Handle date range filter
  const handleDateRangeChange = (e) => {
    const { name, value } = e.target;
    setDateRange((prev) => ({ ...prev, [name]: value }));
  };

  // Handle event selection
  const handleEventToggle = (eventName) => {
    setSelectedEvents((prev) =>
      prev.includes(eventName)
        ? prev.filter((name) => name !== eventName)
        : [...prev, eventName],
    );
  };

  // Filter data
  const filteredPrices = prices.filter(
    (p) =>
      new Date(p.Date) >= new Date(dateRange.start) &&
      new Date(p.Date) <= new Date(dateRange.end),
  );

  const filteredEvents = events.filter(
    (e) =>
      selectedEvents.includes(e.Event) &&
      new Date(e.Date) >= new Date(dateRange.start) &&
      new Date(e.Date) <= new Date(dateRange.end),
  );

  const filteredChangePoints = changePoints.filter(
    (cp) =>
      new Date(cp.Date) >= new Date(dateRange.start) &&
      new Date(cp.Date) <= new Date(dateRange.end),
  );

  return (
    <div className="App">
      <h1>Brent Oil Price Dashboard</h1>

      {/* Date Range Filter */}
      <div style={{ margin: "20px" }}>
        <label>Start Date: </label>
        <input
          type="date"
          name="start"
          value={dateRange.start}
          onChange={handleDateRangeChange}
          min="1987-05-20"
          max="2022-09-30"
        />
        <label style={{ marginLeft: "20px" }}>End Date: </label>
        <input
          type="date"
          name="end"
          value={dateRange.end}
          onChange={handleDateRangeChange}
          min="1987-05-20"
          max="2022-09-30"
        />
      </div>

      {/* Event Filter */}
      <div style={{ margin: "20px" }}>
        <h3>Select Events to Display:</h3>
        {events.map((event) => (
          <label key={event.Event} style={{ marginRight: "15px" }}>
            <input
              type="checkbox"
              checked={selectedEvents.includes(event.Event)}
              onChange={() => handleEventToggle(event.Event)}
            />
            {event.Event}
          </label>
        ))}
      </div>

      {/* Price Chart */}
      <LineChart
        width={800}
        height={400}
        data={filteredPrices}
        margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="Date" />
        <YAxis
          label={{
            value: "Price (USD/barrel)",
            angle: -90,
            position: "insideLeft",
          }}
        />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="Price" stroke="#8884d8" dot={false} />
        {filteredEvents.map((event) => (
          <ReferenceLine
            key={event.Event}
            x={event.Date}
            stroke="red"
            strokeDasharray="3 3"
            label={{
              value: event.Event,
              position: "top",
              fontSize: 10,
              fill: "red",
              angle: 45,
            }}
          />
        ))}
        {filteredChangePoints.map((cp) => (
          <ReferenceLine
            key={cp.Date}
            x={cp.Date}
            stroke="green"
            strokeDasharray="5 5"
            label={{
              value: `${cp.Description} (Mean: ${cp.Mean_Before} → ${cp.Mean_After})`,
              position: "top",
              fontSize: 10,
              fill: "green",
              angle: 45,
            }}
          />
        ))}
      </LineChart>
    </div>
  );
}

export default App;
