import {
  Container,
  Paper,
  Typography,
  Snackbar,
  Alert,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Close';
import {
  DataGrid,
  GridActionsCellItem,
  GridRowModes,
} from '@mui/x-data-grid';
import type {
  GridRowModesModel,
  GridRowId,
  GridColDef,
  GridRowParams,
} from '@mui/x-data-grid';
import { useEffect, useState } from 'react';
import type { AlertColor } from '@mui/material';
import type { UserRecord } from '../../api/admin';
import {
  listUsers,
  updateUser,
  deleteUser,
} from '../../api/admin';

const AdminUsers = () => {
  const [rows, setRows] = useState<UserRecord[]>([]);
  const [rowModesModel, setRowModesModel] = useState<GridRowModesModel>({});
  const [snack, setSnack] = useState<{
    msg: string;
    sev: AlertColor;
  } | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const data = await listUsers();
        setRows(data);
      } catch {
        setSnack({ msg: 'Error al cargar usuarios', sev: 'error' });
      }
    })();
  }, []);

  const handleRowEditStart = (id: GridRowId) => {
    setRowModesModel((prev) => ({
      ...prev,
      [id]: { mode: GridRowModes.Edit },
    }));
  };

  const handleRowEditStop = (id: GridRowId) => {
    setRowModesModel((prev) => ({
      ...prev,
      [id]: { mode: GridRowModes.View },
    }));
  };

  const processRowUpdate = async (newRow: UserRecord) => {
    try {
      const updated = await updateUser(newRow.id, {
        email: newRow.email,
        role: newRow.role,
      });
      setRows((prev) =>
        prev.map((r) => (r.id === updated.id ? updated : r))
      );
      setSnack({ msg: 'Usuario actualizado', sev: 'success' });
      return updated;
    } catch {
      setSnack({ msg: 'Error al actualizar', sev: 'error' });
      throw new Error(); // necesario para revertir cambios
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('¿Eliminar usuario?')) return;
    try {
      await deleteUser(id);
      setRows((prev) => prev.filter((r) => r.id !== id));
      setSnack({ msg: 'Usuario eliminado', sev: 'success' });
    } catch {
      setSnack({ msg: 'Error al eliminar', sev: 'error' });
    }
  };

  const columns: GridColDef<UserRecord>[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    {
      field: 'email',
      headerName: 'Email',
      flex: 1,
      editable: true,
    },
    {
      field: 'role',
      headerName: 'Rol',
      width: 120,
      editable: true,
      type: 'singleSelect',
      valueOptions: ['admin', 'user'],
    },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Acciones',
      width: 120,
      getActions: ({ id }: GridRowParams) => {
        const isEditing = rowModesModel[id]?.mode === GridRowModes.Edit;
        return isEditing
          ? [
              <GridActionsCellItem
                icon={<SaveIcon />}
                label="Guardar"
                onClick={() => handleRowEditStop(id)}
              />,
              <GridActionsCellItem
                icon={<CancelIcon />}
                label="Cancelar"
                onClick={() =>
                  setRowModesModel((prev) => ({
                    ...prev,
                    [id]: {
                      mode: GridRowModes.View,
                      ignoreModifications: true,
                    },
                  }))
                }
                color="inherit"
              />,
            ]
          : [
              <GridActionsCellItem
                icon={<EditIcon />}
                label="Editar"
                onClick={() => handleRowEditStart(id)}
                color="inherit"
              />,
              <GridActionsCellItem
                icon={<DeleteIcon />}
                label="Eliminar"
                onClick={() => handleDelete(Number(id))}
              />,
            ];
      },
    },
  ];

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 3, mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          Panel de Administración – Usuarios
        </Typography>

        <DataGrid
          rows={rows}
          columns={columns}
          autoHeight
          disableRowSelectionOnClick
          editMode="row"
          rowModesModel={rowModesModel}
          onRowEditStop={(_, e) => e.defaultMuiPrevented}
          processRowUpdate={processRowUpdate}
        />
      </Paper>

      {snack && (
        <Snackbar
          open
          autoHideDuration={4000}
          onClose={() => setSnack(null)}
        >
          <Alert severity={snack.sev} onClose={() => setSnack(null)}>
            {snack.msg}
          </Alert>
        </Snackbar>
      )}
    </Container>
  );
};

export default AdminUsers;
