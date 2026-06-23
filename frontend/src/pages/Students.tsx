export type Division = "LS" | "MS" | "HS";

export interface Student {
  id: number;
  student_id: string;
  first_name: string;
  last_name: string;
  preferred_name: string | null;
  email: string | null;
  grade: number | null;
  division: Division | null;
  graduation_year: number | null;
  is_active: boolean;
}

export const DIVISIONS: Division[] = ["LS", "MS", "HS"];

export const DIVISION_LABELS: Record<Division, string> = {
  LS: "Lower School",
  MS: "Middle School",
  HS: "High School",
};

export const GRADES_BY_DIVISION: Record<Division, number[]> = {
  LS: [1, 2, 3, 4, 5],
  MS: [6, 7, 8],
  HS: [9, 10, 11, 12],
};

import React, { useEffect, useState } from "react";
import { getStudents, StudentSummary } from "../api/api";

export default function Students() {
  const [students, setStudents] = useState<StudentSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    getStudents()
      .then((data) => {
        if (mounted) setStudents(data);
      })
      .finally(() => mounted && setLoading(false));
    return () => {
      mounted = false;
    };
  }, []);

  return (
    <div style={{ padding: 16 }}>
      <h2>Students</h2>
      {loading ? (
        <div>Loading…</div>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ textAlign: "left", padding: 8 }}>Name</th>
              <th style={{ textAlign: "left", padding: 8 }}>Grade</th>
              <th style={{ textAlign: "left", padding: 8 }}>Division</th>
              <th style={{ textAlign: "left", padding: 8 }}>Active</th>
            </tr>
          </thead>
          <tbody>
            {students.map((s) => (
              <tr key={s.id}>
                <td style={{ padding: 8 }}>{s.preferred_name ?? `${s.first_name} ${s.last_name}`}</td>
                <td style={{ padding: 8 }}>{s.grade ?? "—"}</td>
                <td style={{ padding: 8 }}>{s.division ?? "—"}</td>
                <td style={{ padding: 8 }}>{s.is_active ? "Yes" : "No"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}