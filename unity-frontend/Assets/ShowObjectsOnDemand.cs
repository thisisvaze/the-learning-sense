using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Microsoft.MixedReality.Toolkit;
using Microsoft.MixedReality.Toolkit.Subsystems;
using Microsoft.MixedReality.Toolkit.SpatialManipulation;
using Microsoft.MixedReality.Toolkit.Input;
using UnityEngine.Windows.Speech;
using UnityEngine.UI;
using UnityEngine.Networking;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine.Windows.WebCam;
using TMPro;

public class ShowObjectsOnDemand : MonoBehaviour
{
    IDictionary<string,string> modelMap = null;
    private DictationRecognizer m_DictationRecognizer;
    [SerializeField]
    private Text m_Hypotheses;
    public GameObject[] buttons = new GameObject[10];
    public GameObject labels;
    public Transform cam;
    string APP_ID = "TT3P62-W479LAP7E3";
    [SerializeField]
    private Text m_Recognitions;
    void Start()
    {

    bool earthShown = false, moonShown = false, marsShown = false, saturnShown = false;
    modelMap = new Dictionary<string, string>(){
	{"earth",   Application.dataPath + "/Resources/earth.glb"},
    {"moon",   Application.dataPath + "/Resources/moon.glb"},
    {"mars",   Application.dataPath + "/Resources/mars.glb"},
    {"saturn",   Application.dataPath + "/Resources/saturn.glb"}
      };
    // var phraseRecognitionSubsystem = XRSubsystemHelpers.GetFirstRunningSubsystem<PhraseRecognitionSubsystem>();

    //     // If we found one...
    //     if (phraseRecognitionSubsystem != null)
    //     {
    //         // Register a phrase and its associated action with the subsystem
    //         phraseRecognitionSubsystem.CreateOrGetEventForPhrase("hey").AddListener(() =>
    //         {Debug.Log("Phrase recognized");m_DictationRecognizer.Start();
    //         });
    //         phraseRecognitionSubsystem.CreateOrGetEventForPhrase("cube").AddListener(() =>ImportGLTF("https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Cube/glTF/Cube.gltf", 1) );
    //         phraseRecognitionSubsystem.CreateOrGetEventForPhrase("sphere").AddListener(() => generateSphere());

    //         foreach (var mapItem in modelMap)
    //         {   
    //              phraseRecognitionSubsystem.CreateOrGetEventForPhrase(mapItem.Key).AddListener(() => generateCustomFromURL(mapItem.Value, scale));
    //         }
    
    //     }
       
        m_DictationRecognizer = new DictationRecognizer();

        m_DictationRecognizer.DictationResult += (text, confidence) =>
        {
            if(text.Length>0){
            
           StartCoroutine(GetWolframResults(text));
               
            }
            Debug.LogFormat("Dictation result: {0}", text);
            m_Recognitions.text += text + "\n";
        };

        m_DictationRecognizer.DictationHypothesis += (text) =>
        {
            Debug.LogFormat("Dictation hypothesis: {0}", text);
             float scale = 0.1f;
                if(text.Contains("earth") && earthShown==false){
                generateCustomFromURL(modelMap["earth"], 0.1f);
                earthShown = true;
                }
                if(text.Contains("moon") && moonShown==false){
                generateCustomFromURL(modelMap["moon"], 0.0005f);
                moonShown = true;
                }
                if(text.Contains("mars") && marsShown==false){
                generateCustomFromURL(modelMap["mars"], 0.2f);
                marsShown = true;
                }
                if(text.Contains("saturn") && saturnShown==false){
                generateCustomFromURL(modelMap["saturn"], 0.0001f);
                saturnShown = true;
                }

           // m_Hypotheses.text += text;
        };

        m_DictationRecognizer.DictationComplete += (completionCause) =>
        {
              switch (completionCause)
              {
              case DictationCompletionCause.TimeoutExceeded:
              case DictationCompletionCause.PauseLimitExceeded:
              case DictationCompletionCause.Canceled:
              case DictationCompletionCause.Complete:
              // Restart required
               m_DictationRecognizer.Stop();
               m_DictationRecognizer.Start();
              break;
              case DictationCompletionCause.UnknownError:
              case DictationCompletionCause.AudioQualityFailure:
              case DictationCompletionCause.MicrophoneUnavailable:
              case DictationCompletionCause.NetworkFailure:
              // Error
              m_DictationRecognizer.Stop();
              break;
              }
            
        };

        m_DictationRecognizer.DictationError += (error, hresult) =>
        {
            Debug.LogErrorFormat("Dictation error: {0}; HResult = {1}.", error, hresult);
        };

       m_DictationRecognizer.Start();
        m_DictationRecognizer.AutoSilenceTimeoutSeconds = 15f;
       // m_DictationRecognizer.InitialSilenceTimeoutSeconds = float.PositiveInfinity;
       // ImportGLTF("https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Cube/glTF/Cube.gltf");
        
     //generateCustomFromURL(modelMap["earth"]);
   
    }
    void generateCustomFromURL(string url, float scale)
    {
        Debug.Log("Generate planets GLTF");
        ImportGLTF(url, scale);
    }

    void ImportGLTF(string filepath, float scale) {
        var empty = new GameObject(); 
        var gltf = empty.AddComponent<GLTFast.GltfAsset>();
        gltf.url = filepath;

        Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward*0.5f;
        Vector3 finalPosition = Camera.main.transform.position + forwardPosition;
        gltf.transform.localPosition = finalPosition;
        //gltf.transform.localScale = new Vector3(1f, 1f, 1f);
        empty.transform.localScale = new Vector3(scale, scale, scale);
        empty.AddComponent<BoxCollider>();
        empty.AddComponent<BoundsControl>();
        empty.AddComponent<ObjectManipulator>();
        empty.AddComponent<ConstraintManager>();
        
        Debug.Log("Generatated");
    }


    void generateSphere() {
        Debug.Log("Sphere");
        GameObject sphere = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        sphere.transform.position = new Vector3(-0.1f, 0, 2);
        sphere.transform.localScale = new Vector3(0.3f, 0.3f, 0.3f);
        sphere.AddComponent<BoundsControl>();
        sphere.AddComponent<ObjectManipulator>();
        sphere.AddComponent<ConstraintManager>();
    }
    // void generateCube()
    // {
    //     Debug.Log("Cube");
    //     GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
    //     cube.transform.position = new Vector3(0.3f, 0f, 2);
    //     cube.transform.localScale = new Vector3(0.3f, 0.3f, 0.3f);
    //     cube.AddComponent<BoundsControl>();
    //     cube.AddComponent<ObjectManipulator>();
    //     cube.AddComponent<ConstraintManager>();
    //     cube.AddComponent<ArticulatedHandController>();
    //     //Packages/com.microsoft.mrtk.spatialmanipulation/BoundsControl/Prefabs/BoundingBox.prefab
    // }

    // Update is called once per frame
    void Update()
    {
        
    }

 void OnDestroy()
   {
      if (m_DictationRecognizer != null)
      {
         m_DictationRecognizer.Dispose();
      }
   }
     IEnumerator GetWolframResults(string query)
    {
        
        UnityWebRequest req = UnityWebRequest.Get("http://api.wolframalpha.com/v1/result?appid="+APP_ID+"&i="+System.Web.HttpUtility.UrlEncode(query));
        yield return req.SendWebRequest();
        if (req.result != UnityWebRequest.Result.Success)
        {
            if (req.isNetworkError || req.isHttpError || req.isNetworkError)
                print("Error: " + req.error);
        }
        else
        {
            

            Debug.Log(req.downloadHandler.text);
            //Vector3 cameraRelative = cam.TransformPoint((float.Parse(labelInfo.x) - 0.5f) / 3 , (float.Parse(labelInfo.y) - 0.5f )/ 3 , 1.5f);
            //
            Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
            Vector3 finalPosition = Camera.main.transform.position + 0.5f*forwardPosition;
            Debug.Log(finalPosition);
            int i = 0;
            if(buttons[i] == null){
                buttons[i] = (Instantiate(labels,  finalPosition ,Camera.main.transform.rotation));
            }
            
            buttons[i].GetComponentInChildren<TMP_Text>().text = req.downloadHandler.text;



        }

        //     //LabelInfo[] info = JsonHelper.FromJson<LabelInfo>(req.downloadHandler.text);
        //     if (1 > 0) {

        //         //Debug.Log(info[0].name);
        //         foreach (GameObject button in buttons)
        //         {
        //             Destroy(button);
        //         }
        //         buttons = new GameObject[info.Length];
        //         // int i = 0;
                
        //         // foreach (LabelInfo labelInfo in info)
        //         // {
        //         //     //Vector3 cameraRelative = cam.TransformPoint((float.Parse(labelInfo.x) - 0.5f) / 3 , (float.Parse(labelInfo.y) - 0.5f )/ 3 , 1.5f);
        //         //     //
        //         //     Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward;
        //         //     Vector3 finalPosition = Camera.main.transform.position + forwardPosition + new Vector3((float.Parse(labelInfo.x) - 0.5f) , (float.Parse(labelInfo.y) - 0.5f) , 0);
        //         //     Debug.Log(finalPosition);
        //         //     //
        //         //     buttons[i] = (Instantiate(labels, finalPosition,Camera.main.transform.rotation));
        //         //     buttons[i].GetComponentInChildren<TMP_Text>().text = labelInfo.name;
        //         //     i++;
        //         // }
        //     }
        // }
             
       // yield return new WaitForSeconds(5);
        //StartCoroutine(GetScreenshotFromHololens());
    }
}
