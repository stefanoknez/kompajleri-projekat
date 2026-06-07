class Main inherits IO {
    copy_me() : SELF_TYPE { self };
    make() : SELF_TYPE { new SELF_TYPE };
    main() : Object {
        {
            -- copy() returns SELF_TYPE; on a Main receiver, result is Main
            out_string("ok");
            copy_me();
        }
    };
};
