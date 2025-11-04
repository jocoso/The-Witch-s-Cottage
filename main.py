from lib.bodyparts import Mouth, Brain, Ears

# glb
if __name__ == "__main__":
    # God Init
    glb_mth = Mouth()
    glb_eas = Ears()
    glb_brn = Brain(mth=glb_mth, eas=glb_eas)

    glb_brn.run()
