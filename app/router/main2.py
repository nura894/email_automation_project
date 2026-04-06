from fastapi import UploadFile, File, APIRouter, Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import io
import logging
import time

from app.csv_cleaning import clean_csv_from_df
from app.template_engine import render_template, subject_template, body_template
from app.email_sender import send_email
from app.utils.security import decrypt_password
from app.utils.dependencies import get_current_user

# Logging setup
logging.basicConfig(
    filename="app/email_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

router= APIRouter(prefix="/upload_csv", tags=["Upload_csv"])


def send_with_retry(lead, user, real_password, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            subject = render_template(subject_template, lead)
            body = render_template(body_template, lead)

            res=send_email(
                sender = user.email,
                password=real_password,
                receiver=lead["email"],
                subject=subject,
                body=body
            )

            if res['success']:
                logging.info(f"Email sent to {lead['email']}")
                return True
            else: 
                logging.warning(f"Attempt {attempt} failed for {lead['email']} - {res['error']}")

        except Exception as e:
            logging.warning(f"Attempt {attempt} failed for {lead['email']} - {str(e)}")
            

    logging.error(f"Failed after retries: {lead['email']}")
    return False

@router.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...),
                     user= Depends(get_current_user)):
    
    try:
        # Validate file type
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files allowed")

        contents = await file.read()

        try:
            df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid CSV format")

        if df.empty:
            raise HTTPException(status_code=400, detail="CSV is empty")

        # Clean data
        df = clean_csv_from_df(df)

        real_password = decrypt_password(user.smtp_password)

        failed_leads = []
        success_leads=[]

        for _, row in df.iterrows():
            lead = row.to_dict()

            success = send_with_retry(lead,user, real_password)

            if not success:
                failed_leads.append(lead)
                
            if success:
                success_leads.append(lead)    

        # Save failed emails
        # if failed_leads:
        #     pd.DataFrame(failed_leads).to_csv("failed_emails.csv", index=False)

        return JSONResponse(
            status_code=200,
            content={
                "status": "completed",
                "total": len(success_leads),
                "failed": len(failed_leads)
            }
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        logging.exception("Full error:")
        raise HTTPException(status_code=500, detail='Internal server error')