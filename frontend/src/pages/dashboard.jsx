import { useEffect, useRef, useState } from "react";
import api from "../api/client";

function Dashboard({ onLogout, onOpenDocument }) {
  const fileInputRef = useRef(null);
  const documentsSectionRef = useRef(null);
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadDocuments = async () => {
    try {
      const response = await api.get("/pdf/my-documents");
      setDocuments(response.data);
    } catch (err) {
      console.error("DOCUMENT LOAD ERROR:", err.response?.data);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0];

    if (!file) {
      return;
    }

    setError("");
    setSuccess("");

    if (file.type !== "application/pdf") {
      setError("Only PDF files are allowed.");
      e.target.value = "";
      return;
    }

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await api.post(
        "/pdf/upload",
        formData
      );

      setSuccess(
        `"${response.data.filename}" uploaded and indexed successfully.`
      );

      await loadDocuments();
    } catch (err) {
      console.error("UPLOAD ERROR:", err.response?.data);

      const detail = err.response?.data?.detail;

      if (Array.isArray(detail)) {
        setError(
          detail.map((item) => item.msg).join(", ")
        );
      } else {
        setError(
          detail ||
            err.response?.data?.error ||
            "Upload failed. Please try again."
        );
      }
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  };
const handleDelete = async (document) => {
  const confirmed = window.confirm(
    `Are you sure you want to delete "${document.filename}"?`
  );

  if (!confirmed) {
    return;
  }

  setError("");
  setSuccess("");

  try {
    await api.delete(`/pdf/${document.document_id}`);

    setDocuments((previous) =>
      previous.filter(
        (item) => item.document_id !== document.document_id
      )
    );

    setSuccess(`"${document.filename}" deleted successfully.`);
  } catch (err) {
    console.error("DELETE ERROR:", err.response?.data);

    const detail = err.response?.data?.detail;

    setError(
      detail || "Could not delete the document. Please try again."
    );
  }
};
  return (
    <div className="dashboard-page">

      <aside className="sidebar">

        <div className="sidebar-brand">
          <div className="brand-icon">✦</div>
          <span>DocMind AI</span>
        </div>

        <nav className="sidebar-nav">
          <button className="nav-item active">
            <span>⌂</span>
            Dashboard
          </button>

          <button
  className="nav-item"
  onClick={() => {
    documentsSectionRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }}
>
  <span>▣</span>
  Documents
</button>
        </nav>

        <button
          className="logout-button"
          onClick={onLogout}
        >
          <span>↪</span>
          Logout
        </button>

      </aside>

      <main className="dashboard-main">

        <header className="dashboard-header">
          <div>
            <p className="eyebrow">YOUR WORKSPACE</p>
            <h1>Welcome back 👋</h1>
            <p className="dashboard-subtitle">
              Manage your documents and explore them with AI.
            </p>
          </div>
        </header>

        {error && (
          <div className="dashboard-alert error-alert">
            {error}
          </div>
        )}

        {success && (
          <div className="dashboard-alert success-alert">
            {success}
          </div>
        )}

        <section className="dashboard-grid">

          <div className="upload-card">
            <div className="card-icon">↑</div>

            <h2>Upload a document</h2>

            <p>
              Add a PDF to your workspace and start
              asking questions about it.
            </p>

            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,application/pdf"
              onChange={handleFileChange}
              style={{ display: "none" }}
            />

            <button
              className="primary-button upload-button"
              onClick={handleUploadClick}
              disabled={uploading}
            >
              {uploading
                ? "Uploading..."
                : "+ Upload PDF"}
            </button>
          </div>

          <div className="stat-card">
            <div className="stat-header">
              <span>Documents</span>
              <span className="stat-icon">▣</span>
            </div>

            <div className="stat-number">
              {documents.length}
            </div>

            <p>
              Documents in your workspace
            </p>
          </div>

        </section>

        <section className="recent-section"
        ref={documentsSectionRef}
>

          <div className="section-header">
            <div>
              <h2>Recent documents</h2>
              <p>
                Your uploaded files will appear here.
              </p>
            </div>
          </div>

          {documents.length === 0 ? (
            <div className="empty-state">

              <div className="empty-icon">▤</div>

              <h3>No documents yet</h3>

              <p>
                Upload your first PDF to start using
                DocMind AI.
              </p>

              <button
                className="secondary-button"
                onClick={handleUploadClick}
                disabled={uploading}
              >
                Upload your first document
              </button>

            </div>
          ) : (
            <div className="documents-list">
              {documents.map((document) => (
                <div
                  className="document-item"
                  key={document.document_id}
                >
                  <div className="document-icon">
                    PDF
                  </div>

                  <div className="document-info">
                    <h3>{document.filename}</h3>

                    <p>
                      Uploaded document
                    </p>
                  </div>

                  <div className="document-actions">

  <button
    className="document-action"
    onClick={() => onOpenDocument(document)}
  >
    Open
  </button>

  <button
    className="delete-button"
    onClick={() => handleDelete(document)}
  >
    Delete
  </button>

</div>
                </div>
              ))}
            </div>
          )}

        </section>

      </main>

    </div>
  );
}

export default Dashboard;