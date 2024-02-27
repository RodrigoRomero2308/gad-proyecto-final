import {
  IonButton,
  IonContent,
  IonIcon,
  IonLabel,
  IonModal,
  IonRange,
  IonText,
} from "@ionic/react";
import { getCatchyUploadPhrase } from "../data/catchyPhrases";
import styles from "./FileUploadInput.module.css";
import { useEffect, useMemo, useRef, useState } from "react";
import {
  cloudUploadOutline,
  searchOutline,
  settingsOutline,
} from "ionicons/icons";

const getInitialSearchRadius = () => {
  const initialRadius = window.localStorage.getItem("search_radius");

  if (!initialRadius || Number.isNaN(initialRadius)) {
    window.localStorage.setItem("search_radius", "0.5");
    return 0.5;
  }

  return Number(initialRadius);
};

const FileUploadInput = ({
  onFileUpload,
}: {
  onFileUpload: (file: File) => void;
}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const [audioUploaded, setAudioUploaded] = useState<File>();

  const audioUrl = useMemo(
    () => (audioUploaded ? URL.createObjectURL(audioUploaded) : undefined),
    [audioUploaded]
  );

  const [catchyPhrase, setCatchyPhrase] = useState(getCatchyUploadPhrase());

  const [searchRadius, setSearchRadius] = useState(getInitialSearchRadius());

  const updateSearchRadius = (newValue: number) => {
    setSearchRadius(newValue);
    window.localStorage.setItem("search_radius", newValue.toString());
  };

  const modal = useRef<HTMLIonModalElement>(null);

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

  let bottomComponent = (
    <>
      <IonButton onClick={onClick} className="ion-margin" expand="block">
        <IonIcon slot="start" icon={cloudUploadOutline}></IonIcon>
        <IonText>Upload</IonText>
      </IonButton>
    </>
  );

  if (audioUploaded)
    bottomComponent = (
      <>
        <audio
          style={{
            display: "block",
            width: "100%",
          }}
          controls
          autoPlay={false}
        >
          <source src={audioUrl} />
        </audio>
        <IonButton
          onClick={() => onFileUpload(audioUploaded)}
          className="ion-margin"
          expand="block"
        >
          <IonIcon slot="start" icon={searchOutline}></IonIcon>
          <IonText>Search for birds</IonText>
        </IonButton>
      </>
    );

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

            setAudioUploaded(files[0]);
            // return onFileUpload(files[0]);
          }}
          ref={inputRef}
          type="file"
          id="file-upload"
          hidden
        />
      </div>
      <IonButton id="open-modal" className="ion-margin" expand="block">
        <IonIcon slot="start" icon={settingsOutline}></IonIcon>
        <IonText>Cambiar radio de busqueda</IonText>
      </IonButton>
      <IonModal
        ref={modal}
        trigger="open-modal"
        initialBreakpoint={0.25}
        breakpoints={[0, 0.25]}
      >
        <IonContent className="ion-padding">
          <IonLabel>Radius: {searchRadius}</IonLabel>
          <IonRange
            max={1}
            step={0.05}
            value={searchRadius}
            aria-label="Range with ionChange"
            onIonChange={({ detail }) =>
              updateSearchRadius(detail.value as number)
            }
          ></IonRange>
          <IonButton
            onClick={() => {
              modal.current?.setCurrentBreakpoint(0);
            }}
            expand="block"
          >
            Cerrar
          </IonButton>
        </IonContent>
      </IonModal>
      {bottomComponent}
    </>
  );
};

export default FileUploadInput;
