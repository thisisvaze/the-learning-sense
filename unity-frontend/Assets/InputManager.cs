using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Microsoft.MixedReality.Toolkit;
public class InputManager : MonoBehaviour
{

    public Vector3 gazePosition;
    public Vector3 gazeNormalPosition;
    public ControllerLookup controllerLookup;
    int positionInLine;
    bool isValidTarget;
    // Start is called before the first frame update

    GLTFast.GltfAsset gltf, gltf1, gltf2;

    void Start()
    {

        var empty = new GameObject();
        gltf = empty.AddComponent<GLTFast.GltfAsset>();
        gltf.url = Application.dataPath + "/Resources/doughnut.glb";

        Vector3 forwardPosition = Camera.main.transform.rotation * Vector3.forward * 0.5f;
        Vector3 finalPosition = Camera.main.transform.position + forwardPosition;
        gltf.transform.localPosition = finalPosition;
        //gltf.transform.localScale = new Vector3(1f, 1f, 1f);
        gltf.transform.localScale = new Vector3(0.3f, 0.3f, 0.3f);

        // gltf1 = empty.AddComponent<GLTFast.GltfAsset>();
        // gltf1.url = Application.dataPath + "/Resources/earth.glb";

        // Vector3 forwardPosition1 = Camera.main.transform.rotation * Vector3.forward * 0.5f;
        // Vector3 finalPosition1 = Camera.main.transform.position + forwardPosition;
        // gltf1.transform.localPosition = finalPosition;
        // //gltf1.transform.localScale = new Vector3(1f, 1f, 1f);
        // gltf1.transform.localScale = new Vector3(0.02f, 0.02f, 0.02f);

        // gltf2 = empty.AddComponent<GLTFast.GltfAsset>();
        // gltf2.url = Application.dataPath + "/Resources/moon.glb";

        // Vector3 forwardPosition2 = Camera.main.transform.rotation * Vector3.forward * 0.5f;
        // Vector3 finalPosition2 = Camera.main.transform.position + forwardPosition;
        // gltf2.transform.localPosition = finalPosition;
        // //gltf2.transform.localScale = new Vector3(1f, 1f, 1f);
        // gltf2.transform.localScale = new Vector3(0.0005f, 0.0005f, 0.0005f);

    }

    // Update is called once per frame
    void Update()
    {
        Debug.Log(controllerLookup.LeftHandController.transform.position);
        gltf.transform.localPosition = controllerLookup.GazeController.transform.position + 1.3f * controllerLookup.GazeController.transform.forward;
        // try
        // {

        //     gltf1.transform.localPosition = controllerLookup.LeftHandController.transform.position + 1.3f * controllerLookup.LeftHandController.transform.forward;
        //     gltf2.transform.localPosition = controllerLookup.RightHandController.transform.position + 1.3f * controllerLookup.RightHandController.transform.forward;

        // }
        // catch { }
    }
}
