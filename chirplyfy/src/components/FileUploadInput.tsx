import { IonButton, IonIcon, IonText } from "@ionic/react";
import { getCatchyUploadPhrase } from "../data/catchyPhrases";
import styles from "./FileUploadInput.module.css";
import { useEffect, useRef, useState } from "react";
import { cloudUploadOutline } from "ionicons/icons";

const FileUploadInput = ({
  onFileUpload,
}: {
  onFileUpload: (file: File) => void;
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const [catchyPhrase, setCatchyPhrase] = useState(getCatchyUploadPhrase());

  const onClick = () => {
    if (!inputRef.current) return;

    inputRef.current.value = "";
    inputRef.current.click();
  };

  useEffect(() => {
    const timeout = window.setInterval(() => {
      setCatchyPhrase(getCatchyUploadPhrase());
    }, 5000);

    return () => {
      window.clearInterval(timeout);
    };
  }, []);

  return (
    <>
      <div className={styles["file-upload-input"]} onClick={onClick}>
        <div>
          <IonText style={{ display: "block" }} color="primary">
            <h1 style={{ marginTop: 0 }}>{catchyPhrase.main}</h1>
          </IonText>
          <IonText style={{ display: "block" }} color="secondary">
            {catchyPhrase.secondary}
          </IonText>
        </div>

        <input
          onChange={(e) => {
            const files = e.target.files;

            if (!files) return console.error("No files found");

            return onFileUpload(files[0]);
          }}
          ref={inputRef}
          type="file"
          id="file-upload"
          hidden
        />
      </div>
      <IonButton onClick={onClick} className="ion-margin" expand="block">
        <IonIcon slot="start" icon={cloudUploadOutline}></IonIcon>
        <IonText>Upload</IonText>
      </IonButton>
    </>
  );
};

export default FileUploadInput;
