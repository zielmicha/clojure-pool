
public class DupHelper {
    public static native void reopen(String fn, int fileno, boolean write);

    static {
        System.load(System.getenv("POOL_BASEDIR") + "/duphelper.so");
    }
}
