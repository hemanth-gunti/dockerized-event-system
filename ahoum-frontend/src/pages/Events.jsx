import { useEffect, useState } from "react";
import api from "../api/api";

export default function Events() {
  const [events, setEvents] = useState([]);

  const fetchEvents = async () => {
    try {
      const res = await api.get("events/");
      setEvents(res.data);
    } catch (err) {
      console.log(err);
      alert("Failed to load events");
    }
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  const enroll = async (eventId) => {
    try {
      await api.post(`events/${eventId}/enroll/`);
      alert("Enrolled successfully!");

      // 🔥 refresh events so UI updates
      fetchEvents();

    } catch (err) {
      alert(err.response?.data?.detail || "Enrollment failed");
    }
  };

  return (
    <div>
      <h2>Available Events</h2>

      {events.length === 0 && <p>No events available</p>}

      {events.map(event => (
        <div key={event.id} style={{ border: "1px solid #ccc", margin: 10, padding: 10 }}>
          <h3>{event.title}</h3>
          <p>{event.description}</p>
          <p>Starts at: {new Date(event.starts_at).toLocaleString()}</p>
          <p>Capacity: {event.capacity}</p>

          {event.enrolled ? (
            <button disabled>Enrolled</button>
          ) : (
            <button onClick={() => enroll(event.id)}>Enroll</button>
          )}
        </div>
      ))}
    </div>
  );
}
