import { IonButton, IonIcon, IonText } from "@ionic/react";
import { getCatchyUploadPhrase } from "../data/catchyPhrases";
import styles from "./FileUploadInput.module.css";
import { useRef } from "react";
import { cloudUploadOutline } from "ionicons/icons";

const FileUploadInput = ({
  onFileUpload,
}: {
  onFileUpload: (file: File) => void;
}) => {
  const catchyPhrase = getCatchyUploadPhrase();
  const inputRef = useRef<HTMLInputElement>(null);

  const onClick = () => {
    if (!inputRef.current) return;

    inputRef.current.value = "";
    inputRef.current.click();
  };

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
