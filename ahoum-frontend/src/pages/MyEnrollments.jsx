import { useEffect, useState } from "react";
import api from "../api/api";

export default function MyEnrollments() {
  const [data, setData] = useState({ upcoming: [], past: [] });

  useEffect(() => {
    api.get("me/enrollments/").then(res => setData(res.data));
  }, []);

  return (
    <div style={{ padding: "30px", color: "white" }}>
      <h2>Upcoming</h2>
      {data.upcoming.map(e => <p>{e.event}</p>)}

      <h2>Past</h2>
      {data.past.map(e => <p>{e.event}</p>)}
    </div>
  );
}
