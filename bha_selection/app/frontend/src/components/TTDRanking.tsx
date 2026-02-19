import { useState } from "react";
import {
  Box,
  Collapse,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Chip,
} from "@mui/material";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import KeyboardArrowRightIcon from "@mui/icons-material/KeyboardArrowRight";
import type { TTDEntry } from "../types";

interface TTDRankingProps {
  entries: TTDEntry[];
}

function formatHrs(hrs: number): string {
  return hrs < 0.01 ? "<0.01" : hrs.toFixed(2);
}

function formatRop(rop: number): string {
  if (!rop || rop <= 0) return "-";
  return rop.toFixed(0);
}

function formatBitName(mfg?: string, model?: string): string {
  const left = (mfg || "").trim();
  const right = (model || "").trim();
  if (left && right) return `${left} / ${right}`;
  return left || right || "-";
}

function BucketRow({ entry, rank }: { entry: TTDEntry; rank: number }) {
  const [open, setOpen] = useState(false);
  const hasBuckets = entry.buckets && entry.buckets.length > 0;
  const hasBitBreakdown =
    entry.bit_ttd_by_mfg_model && entry.bit_ttd_by_mfg_model.length > 0;
  const hasExpandable = hasBuckets || hasBitBreakdown;

  return (
    <>
      <TableRow
        hover
        onClick={() => hasExpandable && setOpen(!open)}
        sx={{ cursor: hasExpandable ? "pointer" : "default" }}
      >
        <TableCell sx={{ width: 48, pr: 0 }}>
          <Box sx={{ display: "flex", alignItems: "center", gap: 0.25 }}>
            {hasExpandable && (
              <IconButton size="small" sx={{ p: 0, mr: 0.25 }}>
                {open ? (
                  <KeyboardArrowDownIcon sx={{ fontSize: 16 }} />
                ) : (
                  <KeyboardArrowRightIcon sx={{ fontSize: 16 }} />
                )}
              </IconButton>
            )}
            {rank === 1 ? (
              <Chip
                label="1"
                color="success"
                size="small"
                sx={{ fontWeight: 700, minWidth: 24, height: 22 }}
              />
            ) : (
              rank
            )}
          </Box>
        </TableCell>
        <TableCell sx={{ fontFamily: "monospace", fontSize: "0.8rem" }}>
          {entry.group_key}
        </TableCell>
        <TableCell align="right">{entry.num_runs}</TableCell>
        <TableCell align="right">
          {entry.is_rss ? (
            <Chip
              label="RSS"
              size="small"
              color="info"
              sx={{ fontWeight: 600, height: 20, fontSize: "0.7rem" }}
            />
          ) : entry.actual_slide_pct != null && !isNaN(entry.actual_slide_pct) ? (
            `${(entry.actual_slide_pct * 100).toFixed(0)}%`
          ) : (
            "-"
          )}
        </TableCell>
        <TableCell align="right">{entry.ttd_hours.toFixed(1)}</TableCell>
        <TableCell align="right">{entry.ttd_days.toFixed(2)}</TableCell>
      </TableRow>
      {hasExpandable && (
        <TableRow>
          <TableCell sx={{ py: 0, borderBottom: open ? undefined : "none" }} colSpan={6}>
            <Collapse in={open} timeout="auto" unmountOnExit>
              <Box sx={{ py: 1, pl: 2 }}>
                <Box sx={{ mb: 1.25 }}>
                  <Typography variant="caption" sx={{ fontWeight: 600 }}>
                    Common Motor
                  </Typography>
                  <Typography variant="caption" sx={{ display: "block" }}>
                    {entry.common_motor?.label || "-"}
                  </Typography>
                  <Typography variant="caption" color="text.secondary" sx={{ display: "block" }}>
                    Diam: {(entry.common_motor?.motor_diam || "N/A") === "N/A" ? "N/A" : `${entry.common_motor?.motor_diam}"`} | Lobes:{" "}
                    {entry.common_motor?.rotor_lobes || "N/A"}/
                    {entry.common_motor?.stator_lobes || "N/A"} | Stages:{" "}
                    {entry.common_motor?.stages || "N/A"}
                  </Typography>
                </Box>

                <Box sx={{ mb: 1.25 }}>
                  <Typography variant="caption" sx={{ fontWeight: 600 }}>
                    Fastest Bit
                  </Typography>
                  <Typography variant="caption" sx={{ display: "block" }}>
                    {entry.fastest_bit
                      ? formatBitName(
                          entry.fastest_bit.bit_manufacturer,
                          entry.fastest_bit.bit_model
                        )
                      : "-"}
                  </Typography>
                  {entry.fastest_bit && (
                    <Typography
                      variant="caption"
                      color="text.secondary"
                      sx={{ display: "block" }}
                    >
                      {entry.fastest_bit.ttd_hours.toFixed(1)} hrs ({entry.fastest_bit.ttd_days.toFixed(2)} days),{" "}
                      {entry.fastest_bit.num_runs} runs
                    </Typography>
                  )}
                </Box>

                {hasBitBreakdown && (
                  <Box sx={{ mb: 1.25 }}>
                    <Typography variant="caption" sx={{ fontWeight: 600 }}>
                      Bit manufacturer/model TTD (within this equivalent BHA)
                    </Typography>
                    <Table size="small" sx={{ mt: 0.5 }}>
                      <TableHead>
                        <TableRow>
                          <TableCell sx={{ fontWeight: 600, fontSize: "0.75rem", py: 0.5 }}>
                            Manufacturer
                          </TableCell>
                          <TableCell sx={{ fontWeight: 600, fontSize: "0.75rem", py: 0.5 }}>
                            Bit Model
                          </TableCell>
                          <TableCell
                            align="right"
                            sx={{ fontWeight: 600, fontSize: "0.75rem", py: 0.5 }}
                          >
                            Runs
                          </TableCell>
                          <TableCell
                            align="right"
                            sx={{ fontWeight: 600, fontSize: "0.75rem", py: 0.5 }}
                          >
                            TTD (hrs)
                          </TableCell>
                          <TableCell
                            align="right"
                            sx={{ fontWeight: 600, fontSize: "0.75rem", py: 0.5 }}
                          >
                            TTD (days)
                          </TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {entry.bit_ttd_by_mfg_model.map((bit, i) => (
                          <TableRow key={`${bit.bit_manufacturer}-${bit.bit_model}-${i}`}>
                            <TableCell sx={{ fontSize: "0.75rem", py: 0.25 }}>
                              {bit.bit_manufacturer || "-"}
                            </TableCell>
                            <TableCell sx={{ fontSize: "0.75rem", py: 0.25 }}>
                              {bit.bit_model || "-"}
                            </TableCell>
                            <TableCell align="right" sx={{ fontSize: "0.75rem", py: 0.25 }}>
                              {bit.num_runs}
                            </TableCell>
                            <TableCell align="right" sx={{ fontSize: "0.75rem", py: 0.25 }}>
                              {bit.ttd_hours.toFixed(1)}
                            </TableCell>
                            <TableCell align="right" sx={{ fontSize: "0.75rem", py: 0.25 }}>
                              {bit.ttd_days.toFixed(2)}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </Box>
                )}
                {hasBuckets && (
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell sx={{ fontWeight: 600, fontSize: "0.75rem", py: 0.5 }}>
                          Bucket
                        </TableCell>
                        <TableCell
                          align="right"
                          sx={{ fontWeight: 600, fontSize: "0.75rem", py: 0.5 }}
                        >
                          Length (ft)
                        </TableCell>
                        <TableCell
                          align="right"
                          sx={{ fontWeight: 600, fontSize: "0.75rem", py: 0.5 }}
                        >
                          Rot. ROP
                        </TableCell>
                        <TableCell
                          align="right"
                          sx={{ fontWeight: 600, fontSize: "0.75rem", py: 0.5 }}
                        >
                          Rot. Time
                        </TableCell>
                        <TableCell
                          align="right"
                          sx={{ fontWeight: 600, fontSize: "0.75rem", py: 0.5 }}
                        >
                          Sld. ROP
                        </TableCell>
                        <TableCell
                          align="right"
                          sx={{ fontWeight: 600, fontSize: "0.75rem", py: 0.5 }}
                        >
                          Sld. Time
                        </TableCell>
                        <TableCell
                          align="right"
                          sx={{ fontWeight: 600, fontSize: "0.75rem", py: 0.5 }}
                        >
                          Total (hrs)
                        </TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {entry.buckets.map((b, i) => {
                        const ropWarning = b.rotary_rop > 500 || b.slide_rop > 500;
                        return (
                          <TableRow
                            key={i}
                            sx={
                              ropWarning
                                ? { bgcolor: "rgba(255, 152, 0, 0.12)" }
                                : undefined
                            }
                          >
                            <TableCell
                              sx={{ fontSize: "0.75rem", py: 0.25, whiteSpace: "nowrap" }}
                            >
                              {b.label}
                              {ropWarning && (
                                <Chip
                                  label="!"
                                  size="small"
                                  color="warning"
                                  sx={{
                                    ml: 0.5,
                                    height: 16,
                                    fontSize: "0.6rem",
                                    fontWeight: 700,
                                  }}
                                />
                              )}
                            </TableCell>
                            <TableCell align="right" sx={{ fontSize: "0.75rem", py: 0.25 }}>
                              {b.length_ft.toLocaleString()}
                            </TableCell>
                            <TableCell align="right" sx={{ fontSize: "0.75rem", py: 0.25 }}>
                              {formatRop(b.rotary_rop)}
                            </TableCell>
                            <TableCell align="right" sx={{ fontSize: "0.75rem", py: 0.25 }}>
                              {formatHrs(b.rotary_time)}
                            </TableCell>
                            <TableCell align="right" sx={{ fontSize: "0.75rem", py: 0.25 }}>
                              {formatRop(b.slide_rop)}
                            </TableCell>
                            <TableCell align="right" sx={{ fontSize: "0.75rem", py: 0.25 }}>
                              {formatHrs(b.slide_time)}
                            </TableCell>
                            <TableCell
                              align="right"
                              sx={{ fontSize: "0.75rem", py: 0.25, fontWeight: 600 }}
                            >
                              {formatHrs(b.total_time)}
                            </TableCell>
                          </TableRow>
                        );
                      })}
                    </TableBody>
                  </Table>
                )}
              </Box>
            </Collapse>
          </TableCell>
        </TableRow>
      )}
    </>
  );
}

export default function TTDRanking({ entries }: TTDRankingProps) {
  if (entries.length === 0) {
    return (
      <Typography variant="body2" color="text.secondary">
        No TTD results available.
      </Typography>
    );
  }

  return (
    <Box>
      <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
        Time to TD Ranking
      </Typography>
      <TableContainer sx={{ maxHeight: 600 }}>
        <Table size="small" stickyHeader>
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 600, width: 48 }}>#</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Equiv. BHA</TableCell>
              <TableCell sx={{ fontWeight: 600 }} align="right">
                Runs
              </TableCell>
              <TableCell sx={{ fontWeight: 600 }} align="right">
                Slide %
              </TableCell>
              <TableCell sx={{ fontWeight: 600 }} align="right">
                TTD (hrs)
              </TableCell>
              <TableCell sx={{ fontWeight: 600 }} align="right">
                TTD (days)
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {entries.map((entry, idx) => (
              <BucketRow key={idx} entry={entry} rank={idx + 1} />
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}
