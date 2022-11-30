// TODO: [Optional] Add copyright and license statement(s).

using Microsoft.MixedReality.Toolkit;
using Microsoft.MixedReality.Toolkit.Subsystems;
using UnityEngine;
using UnityEngine.Scripting;

namespace thelearningdimesion.MRTK3.Subsystems
{
    [Preserve]
    [MRTKSubsystem(
        Name = "thelearningdimesion.mrtk3.subsystems",
        DisplayName = "thelearningdimesion NewSubsystem",
        Author = "thelearningdimesion",
        ProviderType = typeof(thelearningdimesionNewSubsystemProvider),
        SubsystemTypeOverride = typeof(thelearningdimesionNewSubsystem),
        ConfigType = typeof(BaseSubsystemConfig))]
    public class thelearningdimesionNewSubsystem : NewSubsystem
    {
        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
        static void Register()
        {
            // Fetch subsystem metadata from the attribute.
            var cinfo = XRSubsystemHelpers.ConstructCinfo<thelearningdimesionNewSubsystem, NewSubsystemCinfo>();

            if (!thelearningdimesionNewSubsystem.Register(cinfo))
            {
                Debug.LogError($"Failed to register the {cinfo.Name} subsystem.");
            }
        }

        [Preserve]
        class thelearningdimesionNewSubsystemProvider : Provider
        {

            #region INewSubsystem implementation

            // TODO: Add the provider implementation.

            #endregion NewSubsystem implementation
        }
    }
}
