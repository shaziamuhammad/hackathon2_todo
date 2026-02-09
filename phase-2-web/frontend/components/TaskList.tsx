import { Task } from '@/types/task'
import { useState } from 'react'

interface TaskListProps {
  tasks: Task[];
  onUpdate: (id: string, updatedTask: Partial<Task>) => void;
  onDelete: (id: string) => void;
  onToggleComplete: (id: string, completed: boolean) => void;
  loading: boolean;
}

export default function TaskList({ tasks, onUpdate, onDelete, onToggleComplete, loading }: TaskListProps) {
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editTitle, setEditTitle] = useState('')
  const [editDescription, setEditDescription] = useState('')

  const startEditing = (task: Task) => {
    setEditingId(task.id)
    setEditTitle(task.title)
    setEditDescription(task.description || '')
  }

  const saveEdit = (id: string) => {
    if (editTitle.trim()) {
      onUpdate(id, {
        title: editTitle.trim(),
        description: editDescription.trim() || undefined
      })
      setEditingId(null)
    }
  }

  const cancelEdit = () => {
    setEditingId(null)
  }

  if (loading && tasks.length === 0) {
    return <div className="text-center py-4">Loading tasks...</div>
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <div
          key={task.id}
          className={`p-4 rounded-lg border ${
            task.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'
          } shadow-sm`}
        >
          <div className="flex items-start justify-between">
            <div className="flex items-start space-x-3">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => onToggleComplete(task.id, !task.completed)}
                className="mt-1 h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
                aria-label={`Mark task "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
              />
              <div>
                {editingId === task.id ? (
                  <div className="space-y-2">
                    <input
                      type="text"
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                      className="w-full border rounded px-2 py-1 text-gray-900 bg-white"
                      placeholder="Task title"
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') saveEdit(task.id)
                        if (e.key === 'Escape') cancelEdit()
                      }}
                      autoFocus
                    />
                    <textarea
                      value={editDescription}
                      onChange={(e) => setEditDescription(e.target.value)}
                      className="w-full border rounded px-2 py-1 text-gray-900 bg-white"
                      placeholder="Task description (optional)"
                      rows={2}
                      onKeyDown={(e) => {
                        if (e.key === 'Escape') cancelEdit()
                      }}
                    />
                    <div className="flex space-x-2">
                      <button
                        onClick={() => saveEdit(task.id)}
                        className="bg-blue-500 text-white px-3 py-1 rounded text-sm"
                      >
                        Save
                      </button>
                      <button
                        onClick={cancelEdit}
                        className="bg-gray-500 text-white px-3 py-1 rounded text-sm"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  <>
                    <h3 className={`font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                      {task.title}
                    </h3>
                    {task.description && (
                      <p className={`mt-1 text-sm ${task.completed ? 'line-through text-gray-400' : 'text-gray-600'}`}>
                        {task.description}
                      </p>
                    )}
                    <p className="mt-2 text-xs text-gray-500">
                      Created: {new Date(task.created_at).toLocaleDateString()}
                    </p>
                  </>
                )}
              </div>
            </div>
            <div className="flex space-x-2">
              {editingId !== task.id && (
                <>
                  <button
                    onClick={() => startEditing(task)}
                    className="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => onDelete(task.id)}
                    className="text-red-600 hover:text-red-800 text-sm"
                  >
                    Delete
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}