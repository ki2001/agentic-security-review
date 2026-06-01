from flask import Flask, jsonify, request, send_file
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-do-not-use"

INVOICES = {
    "inv_1": {"org_id": "org_a", "amount": 1000, "patient": "Demo Patient A"},
    "inv_2": {"org_id": "org_b", "amount": 2500, "patient": "Demo Patient B"},
}


def current_user():
    return {"id": "user_a", "org_id": request.headers.get("X-Org", "org_a"), "role": "user"}


@app.get("/invoices/<invoice_id>")
def get_invoice(invoice_id):
    # Vulnerable: trusts user-supplied org_id instead of deriving authorization from session.
    org_id = request.args.get("org_id")
    invoice = INVOICES.get(invoice_id)
    if not invoice or invoice["org_id"] != org_id:
        return jsonify({"error": "not found"}), 404
    return jsonify(invoice)


@app.get("/download")
def download():
    # Vulnerable: path traversal allows reading files outside ./reports.
    name = request.args.get("name", "sample.txt")
    return send_file(os.path.join("reports", name))


@app.post("/resize")
def resize_image():
    # Vulnerable: command injection via unsanitized filename.
    filename = request.json.get("filename", "image.png")
    os.system(f"convert uploads/{filename} -resize 100x100 /tmp/out.png")
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)
