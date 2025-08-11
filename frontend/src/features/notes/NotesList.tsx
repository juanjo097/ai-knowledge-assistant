import * as React from "react";
import {
  Card,
  CardHeader,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Typography,
  Divider,
} from "@mui/material";
import { listNotes } from "../../shared/api/endpoints";

type Row = { id: number; title: string; created_at: string };

export default function NotesList() {
  const [rows, setRows] = React.useState<Row[]>([]);
  const [loaded, setLoaded] = React.useState(false);

  React.useEffect(() => {
    let mounted = true;
    listNotes()
      .then((data) => {
        if (mounted) {
          setRows(data);
          setLoaded(true);
        }
      })
      .catch(() => setLoaded(true));
    return () => {
      mounted = false;
    };
  }, []);

  return (
    <Card variant="outlined">
      <CardHeader title="Notes" subheader={loaded ? undefined : "Loading…"} />
      <CardContent sx={{ pt: 0 }}>
        {rows.length === 0 ? (
          <Typography variant="body2" color="text.secondary">
            No notes yet.
          </Typography>
        ) : (
          <List dense disablePadding>
            {rows.map((n, i) => (
              <React.Fragment key={n.id}>
                <ListItem disableGutters>
                  <ListItemText
                    primary={n.title}
                    secondary={new Date(n.created_at).toLocaleString()}
                    primaryTypographyProps={{ variant: "body2" }}
                  />
                </ListItem>
                {i < rows.length - 1 && <Divider component="li" />}
              </React.Fragment>
            ))}
          </List>
        )}
      </CardContent>
    </Card>
  );
}
