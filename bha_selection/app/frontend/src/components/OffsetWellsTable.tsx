import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import type { OffsetWell } from "../types";

interface OffsetWellsTableProps {
  wells: OffsetWell[];
}

export default function OffsetWellsTable({ wells }: OffsetWellsTableProps) {
  if (wells.length === 0) {
    return (
      <Typography variant="body2" color="text.secondary">
        No offset wells found for this section.
      </Typography>
    );
  }

  return (
    <TableContainer sx={{ maxHeight: 300 }}>
      <Table size="small" stickyHeader>
        <TableHead>
          <TableRow>
            <TableCell sx={{ fontWeight: 600 }}>Well Name</TableCell>
            <TableCell sx={{ fontWeight: 600 }}>Operator</TableCell>
            <TableCell sx={{ fontWeight: 600 }} align="right">
              Distance (mi)
            </TableCell>
            <TableCell sx={{ fontWeight: 600 }} align="right">
              BHA Runs
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {wells.slice(0, 50).map((w, idx) => (
            <TableRow key={idx} hover>
              <TableCell>{w.well_name || w.asset_id}</TableCell>
              <TableCell>{w.operator}</TableCell>
              <TableCell align="right">{w.distance_miles}</TableCell>
              <TableCell align="right">{w.runs}</TableCell>
            </TableRow>
          ))}
          {wells.length > 50 && (
            <TableRow>
              <TableCell colSpan={4}>
                <Typography variant="caption" color="text.secondary">
                  ... and {wells.length - 50} more wells
                </Typography>
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
