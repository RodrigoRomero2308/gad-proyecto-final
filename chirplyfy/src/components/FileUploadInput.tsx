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
import AudioPlayer from "./AudioPlayer";

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

  if (audioUploaded && audioUrl)
    bottomComponent = (
      <>
        <AudioPlayer url={audioUrl} id="input" />
        <IonButton
          onClick={() => onFileUpload(audioUploaded)}
          className="ion-margin"
          expand="block"
        >
          <IonIcon slot="start" icon={searchOutline}></IonIcon>
          <IonText>Search for birds</IonText>
        </IonButton>
        <IonButton onClick={onClick} className="ion-margin" expand="block">
          <IonIcon slot="start" icon={cloudUploadOutline}></IonIcon>
          <IonText>Use another file</IonText>
        </IonButton>
      </>
    );

  return (
    <>
      <div className={styles["file-upload-input"]} onClick={onClick}>
        <div className={styles["file-upload-input-text"]}>
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
        <IonText>Change search radius</IonText>
      </IonButton>
      <IonModal
        ref={modal}
        trigger="open-modal"
        initialBreakpoint={0.25}
        breakpoints={[0, 0.25]}
      >
        <IonContent className="ion-padding">
          <IonLabel>Radius: {searchRadius}</IonLabel>
          <IonLabel>
            <p>
              Wider search, diverse chirps: Increase the radius to see more, but
              expect variety.
            </p>
          </IonLabel>
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
            Close
          </IonButton>
        </IonContent>
      </IonModal>
      {bottomComponent}
    </>
  );
};

export default FileUploadInput;
